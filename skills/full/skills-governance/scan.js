#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

function parseArgs(argv) {
  const options = {
    mode: 'codex',
    format: 'markdown',
    duplicatesOnly: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === '--mode' && argv[index + 1]) {
      options.mode = argv[index + 1];
      index += 1;
      continue;
    }
    if (value === '--format' && argv[index + 1]) {
      options.format = argv[index + 1];
      index += 1;
      continue;
    }
    if (value === '--duplicates-only') {
      options.duplicatesOnly = true;
    }
  }

  if (!['codex', 'all'].includes(options.mode)) {
    throw new Error(`Unsupported mode: ${options.mode}`);
  }

  if (!['markdown', 'json'].includes(options.format)) {
    throw new Error(`Unsupported format: ${options.format}`);
  }

  return options;
}

function existsDirectory(targetPath) {
  try {
    return fs.statSync(targetPath).isDirectory();
  } catch {
    return false;
  }
}

function existsFile(targetPath) {
  try {
    return fs.statSync(targetPath).isFile();
  } catch {
    return false;
  }
}

function expandHome(targetPath) {
  if (!targetPath) {
    return targetPath;
  }
  if (targetPath === '~') {
    return os.homedir();
  }
  if (targetPath.startsWith('~/')) {
    return path.join(os.homedir(), targetPath.slice(2));
  }
  return targetPath;
}

function normalizePath(targetPath) {
  const expanded = expandHome(targetPath);
  try {
    return fs.realpathSync.native(expanded);
  } catch {
    return path.resolve(expanded);
  }
}

function displayPath(targetPath) {
  const homeDirectory = os.homedir();
  if (targetPath.startsWith(homeDirectory)) {
    return `~${targetPath.slice(homeDirectory.length)}`;
  }
  return targetPath;
}

function findRepoRoot(startDirectory) {
  let currentDirectory = path.resolve(startDirectory);

  while (true) {
    if (existsDirectory(path.join(currentDirectory, '.git'))) {
      return currentDirectory;
    }

    const parentDirectory = path.dirname(currentDirectory);
    if (parentDirectory === currentDirectory) {
      return null;
    }

    currentDirectory = parentDirectory;
  }
}

function collectRepoAgentRoots(startDirectory) {
  const repoRoot = findRepoRoot(startDirectory);
  if (!repoRoot) {
    return [];
  }

  const roots = [];
  let currentDirectory = path.resolve(startDirectory);

  while (true) {
    const candidate = path.join(currentDirectory, '.agents', 'skills');
    if (existsDirectory(candidate)) {
      roots.push({
        kind: 'repo-agents',
        label: 'repo-agents',
        path: candidate,
      });
    }

    if (currentDirectory === repoRoot) {
      break;
    }

    currentDirectory = path.dirname(currentDirectory);
  }

  const seenPaths = new Set();
  return roots.filter((root) => {
    const normalized = normalizePath(root.path);
    if (seenPaths.has(normalized)) {
      return false;
    }
    seenPaths.add(normalized);
    return true;
  });
}

function detectRoots(mode, currentDirectory) {
  const roots = [];
  const addRoot = (kind, label, targetPath) => {
    if (!existsDirectory(targetPath)) {
      return;
    }
    roots.push({ kind, label, path: targetPath });
  };

  addRoot('codex-user', 'codex-user', path.join(os.homedir(), '.codex', 'skills'));
  addRoot('agents-user', 'agents-user', path.join(os.homedir(), '.agents', 'skills'));
  addRoot('codex-admin', 'codex-admin', path.join('/etc', 'codex', 'skills'));

  for (const repoRoot of collectRepoAgentRoots(currentDirectory)) {
    roots.push(repoRoot);
  }

  if (mode === 'all') {
    addRoot('claude-user', 'claude-user', path.join(os.homedir(), '.claude', 'skills'));
    const pluginReposDirectory = path.join(os.homedir(), '.claude', 'plugins', 'repos');
    if (existsDirectory(pluginReposDirectory)) {
      for (const entry of fs.readdirSync(pluginReposDirectory, { withFileTypes: true })) {
        if (!entry.isDirectory()) {
          continue;
        }
        const pluginSkillsDirectory = path.join(pluginReposDirectory, entry.name, 'skills');
        if (!existsDirectory(pluginSkillsDirectory)) {
          continue;
        }
        roots.push({
          kind: 'claude-plugin',
          label: `claude-plugin/${entry.name}`,
          path: pluginSkillsDirectory,
        });
      }
    }
  }

  const dedupedRoots = [];
  const seenPaths = new Set();
  for (const root of roots) {
    const normalized = normalizePath(root.path);
    if (seenPaths.has(normalized)) {
      continue;
    }
    seenPaths.add(normalized);
    dedupedRoots.push(root);
  }
  return dedupedRoots;
}

function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) {
    return {};
  }

  const result = {};
  const lines = match[1].split(/\r?\n/);

  const stripQuotes = (value) => {
    if (!value) {
      return value;
    }
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      return value.slice(1, -1);
    }
    return value;
  };

  const parseBlock = (style, blockLines) => {
    let indent = 0;
    for (const line of blockLines) {
      if (!line.trim()) {
        continue;
      }
      const indentMatch = line.match(/^(\s+)/);
      indent = indentMatch ? indentMatch[1].length : 0;
      break;
    }

    const normalized = blockLines.map((line) => {
      if (!line.trim()) {
        return '';
      }
      if (indent > 0 && line.startsWith(' '.repeat(indent))) {
        return line.slice(indent);
      }
      return line.trimStart();
    });

    if (style === '|') {
      return normalized.join('\n').trimEnd();
    }

    const parts = [];
    let current = [];
    for (const line of normalized) {
      if (!line.trim()) {
        if (current.length > 0) {
          parts.push(current.join(' ').replace(/\s+/g, ' ').trim());
          current = [];
        }
        parts.push('');
        continue;
      }
      current.push(line.trim());
    }
    if (current.length > 0) {
      parts.push(current.join(' ').replace(/\s+/g, ' ').trim());
    }
    return parts.join('\n').trimEnd();
  };

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    if (!line.trim() || /^\s+/.test(line)) {
      continue;
    }

    const matchLine = line.match(/^(\w[\w-]*)\s*:\s*(.*)$/);
    if (!matchLine) {
      continue;
    }

    const key = matchLine[1];
    let value = (matchLine[2] || '').trim();

    if (value === '|' || value === '>') {
      const style = value;
      const blockLines = [];
      for (let nextIndex = index + 1; nextIndex < lines.length; nextIndex += 1) {
        const nextLine = lines[nextIndex];
        if (nextLine.trim() && !/^\s+/.test(nextLine) && /^(\w[\w-]*)\s*:\s*/.test(nextLine)) {
          break;
        }
        blockLines.push(nextLine);
      }
      result[key] = parseBlock(style, blockLines);
      index += blockLines.length;
      continue;
    }

    result[key] = stripQuotes(value);
  }

  return result;
}

function parseSkillsConfig(configPath) {
  if (!existsFile(configPath)) {
    return [];
  }

  const lines = fs.readFileSync(configPath, 'utf8').split(/\r?\n/);
  const entries = [];
  let current = null;

  const flush = () => {
    if (!current || !current.path) {
      current = null;
      return;
    }
    entries.push({
      path: normalizePath(current.path),
      enabled: current.enabled,
    });
    current = null;
  };

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) {
      continue;
    }
    if (line === '[[skills.config]]') {
      flush();
      current = {};
      continue;
    }
    if (/^\[/.test(line)) {
      flush();
      continue;
    }
    if (!current) {
      continue;
    }

    const pair = line.match(/^(\w[\w-]*)\s*=\s*(.+)$/);
    if (!pair) {
      continue;
    }

    const key = pair[1];
    const rawValue = pair[2].trim();
    if (key === 'path') {
      current.path = rawValue.replace(/^"|"$/g, '').replace(/^'|'$/g, '');
      continue;
    }
    if (key === 'enabled') {
      current.enabled = rawValue === 'true';
    }
  }

  flush();
  return entries;
}

function collectSkillDirectories(rootPath) {
  const result = [];
  const visited = new Set();

  const walk = (directory) => {
    const normalized = normalizePath(directory);
    if (visited.has(normalized)) {
      return;
    }
    visited.add(normalized);

    const skillPath = path.join(directory, 'SKILL.md');
    if (existsFile(skillPath)) {
      result.push(directory);
      return;
    }

    let entries = [];
    try {
      entries = fs.readdirSync(directory, { withFileTypes: true });
    } catch {
      return;
    }

    for (const entry of entries) {
      if (!entry.isDirectory()) {
        continue;
      }
      if (entry.name === '.git' || entry.name === 'node_modules' || entry.name === '__pycache__') {
        continue;
      }
      walk(path.join(directory, entry.name));
    }
  };

  walk(rootPath);
  return result;
}

function sourcePriority(kind) {
  if (kind === 'repo-agents') {
    return 100;
  }
  if (kind === 'codex-user') {
    return 90;
  }
  if (kind === 'agents-user') {
    return 80;
  }
  if (kind === 'codex-admin') {
    return 70;
  }
  if (kind === 'codex-system') {
    return 60;
  }
  if (kind === 'claude-user') {
    return 40;
  }
  if (kind === 'claude-plugin') {
    return 20;
  }
  return 10;
}

function buildInventory(options) {
  const roots = detectRoots(options.mode, process.cwd());
  const configEntries = parseSkillsConfig(path.join(os.homedir(), '.codex', 'config.toml'));
  const skills = [];

  for (const root of roots) {
    for (const directory of collectSkillDirectories(root.path)) {
      const skillMdPath = path.join(directory, 'SKILL.md');
      const rawContent = fs.readFileSync(skillMdPath, 'utf8');
      const frontmatter = parseFrontmatter(rawContent);
      const normalizedSkillMdPath = normalizePath(skillMdPath);
      const configEntry = configEntries.find((entry) => entry.path === normalizedSkillMdPath);
      const frontmatterDisabled = String(frontmatter['disable-model-invocation'] || '').trim() === 'true';
      const configDisabled = configEntry ? configEntry.enabled === false : false;
      const flags = [];

      let effectiveKind = root.kind;
      if (normalizedSkillMdPath.includes(`${path.sep}.system${path.sep}`)) {
        effectiveKind = 'codex-system';
      }

      if (frontmatterDisabled) {
        flags.push('frontmatter-disabled');
      }
      if (configDisabled) {
        flags.push('config-disabled');
      }
      if (effectiveKind === 'codex-system') {
        flags.push('system');
      }
      if (root.kind === 'claude-plugin') {
        flags.push('plugin-import');
      }
      if (root.kind === 'claude-user') {
        flags.push('claude-root');
      }

      const lowerPath = directory.toLowerCase();
      if (lowerPath.includes('.bak') || lowerPath.includes('backup') || lowerPath.includes('draft') || lowerPath.includes('final')) {
        flags.push('backup-like');
      }

      skills.push({
        name: frontmatter.name || path.basename(directory),
        description: frontmatter.description || '',
        source: root.label,
        sourceKind: effectiveKind,
        enabled: !(frontmatterDisabled || configDisabled),
        flags: Array.from(new Set(flags)).sort(),
        userInvocable: String(frontmatter['user-invocable'] || '').trim() === 'true',
        path: directory,
        skillMdPath,
        priority: sourcePriority(effectiveKind),
      });
    }
  }

  skills.sort((left, right) => {
    const nameComparison = left.name.localeCompare(right.name);
    if (nameComparison !== 0) {
      return nameComparison;
    }
    return right.priority - left.priority;
  });

  const duplicateMap = new Map();
  for (const skill of skills) {
    if (!duplicateMap.has(skill.name)) {
      duplicateMap.set(skill.name, []);
    }
    duplicateMap.get(skill.name).push(skill);
  }

  const duplicates = Array.from(duplicateMap.entries())
    .filter(([, group]) => group.length > 1)
    .map(([name, group]) => {
      const ordered = [...group].sort((left, right) => right.priority - left.priority || left.path.localeCompare(right.path));
      return {
        name,
        count: ordered.length,
        keepRecommended: {
          source: ordered[0].source,
          path: ordered[0].path,
        },
        skills: ordered.map((skill) => ({
          source: skill.source,
          path: skill.path,
          enabled: skill.enabled,
          flags: skill.flags,
        })),
      };
    })
    .sort((left, right) => right.count - left.count || left.name.localeCompare(right.name));

  const bySourceMap = new Map();
  for (const skill of skills) {
    if (!bySourceMap.has(skill.source)) {
      bySourceMap.set(skill.source, { source: skill.source, total: 0, enabled: 0, disabled: 0 });
    }
    const sourceEntry = bySourceMap.get(skill.source);
    sourceEntry.total += 1;
    if (skill.enabled) {
      sourceEntry.enabled += 1;
    } else {
      sourceEntry.disabled += 1;
    }
  }

  const bySource = Array.from(bySourceMap.values()).sort((left, right) => right.total - left.total || left.source.localeCompare(right.source));
  const suspicious = skills.filter((skill) => skill.flags.some((flag) => ['plugin-import', 'backup-like'].includes(flag)));

  return {
    scannedAt: new Date().toISOString(),
    mode: options.mode,
    roots: roots.map((root) => ({ source: root.label, path: root.path })),
    summary: {
      totalSkills: skills.length,
      enabledSkills: skills.filter((skill) => skill.enabled).length,
      disabledSkills: skills.filter((skill) => !skill.enabled).length,
      duplicateNames: duplicates.length,
      suspiciousSkills: suspicious.length,
    },
    bySource,
    duplicates,
    suspicious,
    skills,
  };
}

function renderMarkdown(report, options) {
  const lines = [];
  lines.push('# Skills Governance Report');
  lines.push('');
  lines.push(`- Scanned at: ${report.scannedAt}`);
  lines.push(`- Mode: ${report.mode}`);
  lines.push(`- Roots: ${report.roots.length}`);
  lines.push(`- Total skills: ${report.summary.totalSkills}`);
  lines.push(`- Enabled: ${report.summary.enabledSkills}`);
  lines.push(`- Disabled: ${report.summary.disabledSkills}`);
  lines.push(`- Duplicate names: ${report.summary.duplicateNames}`);
  lines.push(`- Suspicious skills: ${report.summary.suspiciousSkills}`);
  lines.push('');
  lines.push('## Roots');
  for (const root of report.roots) {
    lines.push(`- ${root.source}: ${displayPath(root.path)}`);
  }
  lines.push('');
  lines.push('## Source Breakdown');
  for (const entry of report.bySource) {
    lines.push(`- ${entry.source}: total ${entry.total}, enabled ${entry.enabled}, disabled ${entry.disabled}`);
  }
  lines.push('');
  lines.push('## Duplicate Names');
  if (report.duplicates.length === 0) {
    lines.push('- none');
  } else {
    for (const duplicate of report.duplicates) {
      lines.push(`- ${duplicate.name} (${duplicate.count}) — keep ${displayPath(duplicate.keepRecommended.path)} from ${duplicate.keepRecommended.source}`);
      for (const skill of duplicate.skills) {
        const flagText = skill.flags.length > 0 ? ` [${skill.flags.join(', ')}]` : '';
        lines.push(`  - ${skill.enabled ? 'enabled' : 'disabled'} · ${skill.source} · ${displayPath(skill.path)}${flagText}`);
      }
    }
  }
  lines.push('');
  lines.push('## Suspicious Flags');
  if (report.suspicious.length === 0) {
    lines.push('- none');
  } else {
    for (const skill of report.suspicious) {
      lines.push(`- ${skill.name} · ${skill.source} · ${displayPath(skill.path)} [${skill.flags.join(', ')}]`);
    }
  }

  if (!options.duplicatesOnly) {
    lines.push('');
    lines.push('## Skills');
    for (const skill of report.skills) {
      const flags = skill.flags.length > 0 ? ` [${skill.flags.join(', ')}]` : '';
      lines.push(`- ${skill.name} · ${skill.enabled ? 'enabled' : 'disabled'} · ${skill.source} · ${displayPath(skill.path)}${flags}`);
    }
  }

  return lines.join('\n');
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  const report = buildInventory(options);
  if (options.duplicatesOnly) {
    report.skills = [];
  }

  if (options.format === 'json') {
    process.stdout.write(JSON.stringify(report, null, 2));
    return;
  }

  process.stdout.write(renderMarkdown(report, options));
}

main();

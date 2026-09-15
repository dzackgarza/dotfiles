from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml


DOTFILES = Path('/home/dzack/dotfiles')


def load_module(name: str, relative: str):
    path = DOTFILES / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_plan(root: Path, card_id: str, *, status: str, archived: bool = False, todos: list[dict] | None = None) -> Path:
    path = root / 'plans' / 'features' / 'FEATURE-test' / 'plans' / card_id / f'{card_id}.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        'id': card_id,
        'title': card_id.replace('PLAN-', '').replace('-', ' ').title(),
        'status': status,
        'archived': archived,
    }
    if todos is not None:
        metadata['todos'] = todos
    path.write_text('---\n' + yaml.safe_dump(metadata, sort_keys=False) + '---\n# Body\n', encoding='utf-8')
    return path


def test_vault_progress_uses_unarchived_current_plan_todos(tmp_path: Path) -> None:
    progress = load_module('vault_progress_test', 'ags/control-panel/scripts/vault-progress.py')
    first = write_plan(
        tmp_path,
        'PLAN-first',
        status='in-progress',
        todos=[
            {'id': 'a', 'content': 'A', 'status': 'complete'},
            {'id': 'b', 'content': 'B', 'status': 'pending'},
        ],
    )
    second = write_plan(
        tmp_path,
        'PLAN-second',
        status='blocked',
        todos=[{'id': 'c', 'content': 'C', 'status': 'complete'}],
    )
    write_plan(
        tmp_path,
        'PLAN-archived',
        status='in-progress',
        archived=True,
        todos=[{'id': 'z', 'content': 'Z', 'status': 'pending'}],
    )
    write_plan(tmp_path, 'PLAN-complete', status='complete')

    result = progress.summarize(str(tmp_path))

    assert result['total'] == 3
    assert result['completed'] == 2
    assert result['percent'] == 66
    assert result['activePlan'] == '2 current plans'
    assert [item['path'] for item in result['activePlans']] == [str(first), str(second)]
    assert [item['status'] for item in result['activePlans']] == ['in-progress', 'blocked']


def test_combined_plan_renderer_names_each_source(tmp_path: Path) -> None:
    renderer = load_module('render_plan_test', 'ags/control-panel/scripts/render-plan.py')
    first = write_plan(tmp_path, 'PLAN-first', status='in-progress')
    second = write_plan(tmp_path, 'PLAN-second', status='blocked')

    combined = renderer.combined_markdown([str(first), str(second)])

    assert '# Current plans' in combined
    assert '## First' in combined
    assert '## Second' in combined
    assert '**Status:** `in-progress`' in combined
    assert '**Status:** `blocked`' in combined
    assert str(first) in combined
    assert str(second) in combined

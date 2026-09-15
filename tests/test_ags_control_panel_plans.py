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


def write_plan(root: Path, card_id: str, *, status: str, archived: bool = False, todos: list[dict] | None = None, description: str = '') -> Path:
    path = root / 'plans' / 'features' / 'FEATURE-test' / 'plans' / card_id / f'{card_id}.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        'id': card_id,
        'title': card_id.replace('PLAN-', '').replace('-', ' ').title(),
        'status': status,
        'archived': archived,
    }
    if description:
        metadata['description'] = description
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
    first = write_plan(tmp_path, 'PLAN-first', status='in-progress', description='Build the first mathematical object.')
    second = write_plan(tmp_path, 'PLAN-second', status='blocked', description='Connect the second object to its upstream model.')

    combined = renderer.combined_markdown([str(first), str(second)])

    assert '# Current plans' in combined
    assert '## First' in combined
    assert '## Second' in combined
    assert '**Status:** `in-progress`' in combined
    assert '**Status:** `blocked`' in combined
    assert '<span class="plan-summary-label">Goal</span>Build the first mathematical object.' in combined
    assert '<span class="plan-summary-label">Goal</span>Connect the second object to its upstream model.' in combined
    assert str(first) in combined
    assert str(second) in combined


def test_dag_renderer_keeps_canonical_graph_and_interactive_browser_engine() -> None:
    renderer = load_module('render_dag_test', 'ags/control-panel/scripts/render-dag.py')
    dag_source = '''## Sequence\n\n```mermaid\ngraph LR\n  FEATURE-one\n  PLAN-one\n  PLAN-two\n  PLAN-one --> PLAN-two\n```\n\n## Dependencies\n\n```mermaid\ngraph LR\n  FEATURE-one\n  PLAN-one\n  PLAN-two\n  PLAN-one --> PLAN-two\n```\n\n## Containment\n\n```mermaid\ngraph LR\n  FEATURE-one\n  PLAN-one\n  FEATURE-one --> PLAN-one\n```\n'''
    sequence = renderer.parse_mermaid_graph(renderer.mermaid_section(dag_source, 'Sequence'))
    deps = renderer.parse_mermaid_graph(renderer.mermaid_section(dag_source, 'Dependencies'))
    containment = renderer.parse_mermaid_graph(renderer.mermaid_section(dag_source, 'Containment'))
    assert sequence == (['FEATURE-one', 'PLAN-one', 'PLAN-two'], [('PLAN-one', 'PLAN-two')])
    assert deps == sequence
    assert containment == (['FEATURE-one', 'PLAN-one'], [('FEATURE-one', 'PLAN-one')])

    template = (DOTFILES / 'ags/control-panel/templates/dag.html').read_text(encoding='utf-8')
    assert '__D3_JS__' in template
    assert '__D3_DAG_JS__' in template
    assert '__GRAPHS_JSON__' in template
    assert 'graphStratify' in template
    assert 'd3.zoom()' in template
    assert 'data-view="sequence"' in template
    assert 'data-view="dependencies"' in template
    assert 'data-view="containment"' in template
    assert 'data-view="pending"' in template
    assert 'plan-dag-view-v3' in template
    assert 'tt-description' in template
    assert 'p.data.description' in template
    payload = renderer.node_payload('PLAN-one', {'PLAN-one': {'title': 'One', 'description': 'Mathematical goal', 'status': 'in-progress'}})
    assert payload['description'] == 'Mathematical goal'
    plan_template = (DOTFILES / 'ags/control-panel/templates/elegant-plan.html').read_text(encoding='utf-8')
    assert '<span class="plan-summary-label">Goal</span>$description$' in plan_template
    assert 'https://d3js.org' not in template
    assert 'unpkg.com/d3-dag' not in template


def test_pending_work_dag_uses_todo_needs_and_goals(tmp_path: Path) -> None:
    renderer = load_module('render_dag_pending_test', 'ags/control-panel/scripts/render-dag.py')
    (tmp_path / 'TODO.md').write_text(
        '- [ ] **`root-work`**. **Needs:** none.\n'
        '  **Goal:** Build the root mathematical object.\n'
        '- [ ] **`dependent-work`**. **Needs:** `root-work`.\n'
        '  **Goal:** Use the root object in the dependent construction.\n'
        '- [x] **`finished-work`**. **Needs:** none.\n',
        encoding='utf-8',
    )
    graph = renderer.pending_todo_graph(tmp_path)
    assert [node['id'] for node in graph['nodes']] == ['root-work', 'dependent-work']
    assert graph['edges'] == [{'from': 'root-work', 'to': 'dependent-work'}]
    by_id = {node['id']: node for node in graph['nodes']}
    assert by_id['root-work']['description'] == 'Build the root mathematical object.'
    assert by_id['root-work']['status'] == 'ready'
    assert by_id['dependent-work']['status'] == 'waiting'


def test_plan_renderer_summarizes_pending_execution_work(tmp_path: Path) -> None:
    renderer = load_module('render_plan_pending_test', 'ags/control-panel/scripts/render-plan.py')
    (tmp_path / 'TODO.md').write_text(
        '- [ ] **`root-work`**. **Needs:** none.\n'
        '  **Goal:** Build the root mathematical object.\n'
        '- [ ] **`dependent-work`**. **Needs:** `root-work`.\n'
        '  **Goal:** Build the dependent object.\n',
        encoding='utf-8',
    )
    records = renderer.pending_work_records(tmp_path)
    assert [record['state'] for record in records] == ['ready', 'waiting']
    # Formatting itself is exercised independently of repo-map lookup.
    assert records[0]['goal'] == 'Build the root mathematical object.'

    template = (DOTFILES / 'ags/control-panel/templates/dag.html').read_text(encoding='utf-8')
    assert 'data-view="pending"' in template
    assert 'Selected work' in template
    assert 'plan-dag-view-v3' in template

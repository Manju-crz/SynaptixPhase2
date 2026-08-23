"""
Prompt Sidecar Manager
Stores all test prompts in a single rest_test/_prompts.json file.

Structure:
{
    "components": {
        "ComponentName": {
            "TestFileName": {
                "class_name": "...",
                "methods": {
                    "test_01_...": "prompt text",
                    ...
                }
            }
        }
    }
}
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

PROMPTS_INDEX = '_prompts.json'


def _normalize_file_name(file_name):
    if file_name and file_name.endswith('.py'):
        return file_name[:-3]
    return file_name or ''


def _index_path(project_root):
    return os.path.join(project_root, 'rest_test', PROMPTS_INDEX)


def _read_index(project_root):
    path = _index_path(project_root)
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Failed to read prompts index {path}: {e}")
        return None


def _write_index(project_root, data):
    path = _index_path(project_root)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to write prompts index {path}: {e}")


def _ensure_index(project_root):
    data = _read_index(project_root)
    if data is None:
        data = {'components': {}}
    return data


def _save_index(index, project_root):
    _write_index(project_root, index)


def _component(index, folder_name, create=False):
    comps = index.setdefault('components', {})
    if create:
        return comps.setdefault(folder_name, {})
    return comps.get(folder_name, {})


def _file_data(index, folder_name, file_name, create=False):
    file_name = _normalize_file_name(file_name)
    comp = _component(index, folder_name, create=create)
    if create:
        return comp.setdefault(file_name, {'methods': {}})
    return comp.get(file_name, {})


def _read_legacy_sidecar(project_root, folder_name, file_name):
    file_name = _normalize_file_name(file_name)
    path = os.path.join(project_root, 'rest_test', folder_name, f'{file_name}_prompts.json')
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Failed to read legacy sidecar {path}: {e}")
        return None


def migrate_existing_sidecars(project_root):
    """Move all per-file *_prompts.json into the single _prompts.json index."""
    rest_test_dir = os.path.join(project_root, 'rest_test')
    if not os.path.isdir(rest_test_dir):
        return

    index = _ensure_index(project_root)
    migrated = False

    for entry in os.listdir(rest_test_dir):
        comp_path = os.path.join(rest_test_dir, entry)
        if not os.path.isdir(comp_path):
            continue

        for fname in os.listdir(comp_path):
            if not fname.endswith('_prompts.json'):
                continue

            file_name = fname[:-13]  # strip '_prompts.json'
            data = _read_legacy_sidecar(project_root, entry, file_name)
            if data:
                target = _file_data(index, entry, file_name, create=True)
                target['class_name'] = data.get('class_name', '')
                target['methods'] = data.get('methods', {})
                migrated = True

            try:
                os.remove(os.path.join(comp_path, fname))
                logger.info(f"🧹 Migrated and removed legacy sidecar: {entry}/{fname}")
            except Exception as e:
                logger.error(f"Failed to remove legacy sidecar {fname}: {e}")

    if migrated:
        _save_index(index, project_root)


def save_prompts(project_root, folder_name, file_name, class_name, prompts):
    """Save or merge prompts for a test file into the index."""
    file_name = _normalize_file_name(file_name)
    index = _ensure_index(project_root)
    file_data = _file_data(index, folder_name, file_name, create=True)

    if class_name:
        file_data['class_name'] = class_name

    file_data['methods'] = {**file_data.get('methods', {}), **prompts}
    _save_index(index, project_root)
    logger.info(f"💾 Saved prompts for {folder_name}/{file_name}")


def load_prompts(project_root, folder_name, file_name):
    """Load prompts for a test file from the index (fallback to legacy sidecar)."""
    file_name = _normalize_file_name(file_name)
    index = _read_index(project_root)
    if not index:
        return _read_legacy_sidecar(project_root, folder_name, file_name)
    return _file_data(index, folder_name, file_name)


def get_prompt(project_root, folder_name, file_name, method_name):
    """Get the prompt for a specific method."""
    file_name = _normalize_file_name(file_name)
    data = load_prompts(project_root, folder_name, file_name)
    if not data:
        return None
    return data.get('methods', {}).get(method_name)


def update_prompt(project_root, folder_name, file_name, class_name, method_name, prompt):
    """Update or add a single method's prompt."""
    file_name = _normalize_file_name(file_name)
    save_prompts(project_root, folder_name, file_name, class_name, {method_name: prompt})


def rename_method(project_root, folder_name, file_name, old_method_name, new_method_name):
    """Rename a method key in the index."""
    file_name = _normalize_file_name(file_name)
    index = _read_index(project_root)
    if not index:
        return

    methods = _file_data(index, folder_name, file_name).get('methods', {})
    if old_method_name in methods:
        methods[new_method_name] = methods.pop(old_method_name)
        _save_index(index, project_root)
        logger.info(f"🔄 Renamed prompt key: {old_method_name} -> {new_method_name}")


def delete_method(project_root, folder_name, file_name, method_name):
    """Remove a method's prompt from the index."""
    file_name = _normalize_file_name(file_name)
    index = _read_index(project_root)
    if not index:
        return

    file_data = _file_data(index, folder_name, file_name)
    methods = file_data.get('methods', {})
    if method_name in methods:
        del methods[method_name]
        _save_index(index, project_root)
        logger.info(f"🗑️ Deleted prompt for method: {method_name}")


def rename_class(project_root, folder_name, file_name, new_class_name):
    """Update the stored class name in the index."""
    file_name = _normalize_file_name(file_name)
    index = _read_index(project_root)
    if not index:
        return

    file_data = _file_data(index, folder_name, file_name)
    if file_data:
        file_data['class_name'] = new_class_name
        _save_index(index, project_root)
        logger.info(f"🏷️ Updated prompt class name to: {new_class_name}")


def rename_file(project_root, folder_name, old_file_name, new_file_name):
    """Rename a file's prompt entry in the index."""
    old_file_name = _normalize_file_name(old_file_name)
    new_file_name = _normalize_file_name(new_file_name)

    index = _read_index(project_root)
    if not index:
        return

    comp = _component(index, folder_name)
    if comp and old_file_name in comp:
        comp[new_file_name] = comp.pop(old_file_name)
        _save_index(index, project_root)
        logger.info(f"📁 Renamed prompt file: {old_file_name} -> {new_file_name}")


def delete_file(project_root, folder_name, file_name):
    """Delete a file's prompt entry from the index."""
    file_name = _normalize_file_name(file_name)

    index = _read_index(project_root)
    if not index:
        return

    comp = _component(index, folder_name)
    if comp and file_name in comp:
        del comp[file_name]
        _save_index(index, project_root)
        logger.info(f"🗑️ Deleted prompts for file: {file_name}")


def rename_component(project_root, old_folder_name, new_folder_name):
    """Rename a component's key in the index."""
    index = _read_index(project_root)
    if not index:
        return

    comp = _component(index, old_folder_name)
    if comp:
        index['components'][new_folder_name] = index['components'].pop(old_folder_name)
        _save_index(index, project_root)
        logger.info(f"🔄 Renamed component prompts: {old_folder_name} -> {new_folder_name}")


def delete_component(project_root, folder_name):
    """Delete a component's prompt entries from the index."""
    index = _read_index(project_root)
    if not index:
        return

    comp = _component(index, folder_name)
    if comp:
        del index['components'][folder_name]
        _save_index(index, project_root)
        logger.info(f"🗑️ Deleted prompts for component: {folder_name}")

import os
import json
from typing import List, Union, Dict, Any


class JSONManager:
    """
    Stateless utility class for working with JSON files using full paths.
    """

    @staticmethod
    def resolve_json_files(path: Union[str, List[str]]) -> List[str]:
        """
        Resolves a path or list of paths into valid JSON file paths.

        Args:
            path (str or List[str]): A directory path, single file path, or list of file paths.

        Returns:
            List[str]: Sorted list of .json file paths.
        """
        if isinstance(path, list):
            return sorted([p for p in path if p.endswith('.json') and os.path.isfile(p)])

        elif os.path.isdir(path):
            return sorted([
                os.path.join(path, f)
                for f in os.listdir(path)
                if f.endswith('.json') and os.path.isfile(os.path.join(path, f))
            ])

        elif os.path.isfile(path) and path.endswith('.json'):
            return [path]

        else:
            raise ValueError("❌ Invalid input path(s). Must be JSON file, list of JSON files, or directory.")

    @staticmethod
    def load_json(path: str) -> Union[Dict[str, Any], List[Any], None]:
        """
        Loads JSON content from a file path.

        Args:
            path (str): Full path to JSON file.

        Returns:
            dict or list or None: Parsed JSON content, or None if load fails.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Failed to load JSON: {path} -> {e}")
            return None

    @staticmethod
    def save_json(path: str, data: Union[Dict[str, Any], List[Any]]) -> None:
        """
        Saves data as JSON to a given path.

        Args:
            path (str): Full path to save the file.
            data (dict or list): Data to serialize.
        """
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"❌ Failed to save JSON: {path} -> {e}")

    @staticmethod
    def load_json_as_list(path: str) -> Union[List[Dict[str, Any]], None]:
        """
        Ensures the loaded JSON is returned as a list of dicts.

        Args:
            path (str): Full path to a JSON file.

        Returns:
            List[dict] or None
        """
        data = JSONManager.load_json(path)
        if isinstance(data, dict):
            return [data]
        elif isinstance(data, list):
            return data
        return None

    @staticmethod
    def delete_file(path: str) -> bool:
        """
        Deletes the file at the given path.

        Args:
            path (str): Full file path.

        Returns:
            bool: True if deleted, False otherwise.
        """
        if os.path.exists(path):
            try:
                os.remove(path)
                return True
            except Exception as e:
                print(f"❌ Failed to delete file: {path} -> {e}")
        return False

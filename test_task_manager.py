
import json
import os
import tempfile
import unittest
from unittest.mock import patch

import task_manager


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tasks_file = os.path.join(
            self.temp_dir.name,
            "tasks.json"
        )

        patcher = patch("task_manager.FILE_NAME", self.tasks_file)
        patcher.start()

        self.addCleanup(patcher.stop)
        self.addCleanup(self.temp_dir.cleanup)

    def test_load_tasks_when_file_does_not_exist(self):
        tasks = task_manager.load_tasks()
        self.assertEqual(tasks, [])

    def test_save_and_load_tasks(self):
        tasks = [
            {"title": "Learn Python", "completed": False}
        ]

        task_manager.save_tasks(tasks)
        loaded_tasks = task_manager.load_tasks()

        self.assertEqual(loaded_tasks, tasks)

    def test_add_task(self):
        tasks = []

        with patch("builtins.input", return_value="Learn Python"):
            with patch("builtins.print"):
                task_manager.add_task(tasks)

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Learn Python")
        self.assertFalse(tasks[0]["completed"])

        with open(self.tasks_file, "r", encoding="utf-8") as file:
            saved_tasks = json.load(file)

        self.assertEqual(saved_tasks, tasks)

    def test_add_task_rejects_empty_title(self):
        tasks = []

        with patch("builtins.input", return_value="   "):
            with patch("builtins.print"):
                task_manager.add_task(tasks)

        self.assertEqual(tasks, [])
        self.assertFalse(os.path.exists(self.tasks_file))

    def test_complete_task(self):
        tasks = [
            {"title": "Learn Python", "completed": False}
        ]

        task_manager.save_tasks(tasks)

        with patch("builtins.input", return_value="1"):
            with patch("builtins.print"):
                task_manager.complete_task(tasks)

        self.assertTrue(tasks[0]["completed"])
        self.assertEqual(task_manager.load_tasks(), tasks)

    def test_delete_task(self):
        tasks = [
            {"title": "Learn Python", "completed": False},
            {"title": "Practice Git", "completed": False}
        ]

        task_manager.save_tasks(tasks)

        with patch("builtins.input", return_value="1"):
            with patch("builtins.print"):
                task_manager.delete_task(tasks)

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Practice Git")
        self.assertEqual(task_manager.load_tasks(), tasks)


if __name__ == "__main__":
    unittest.main()

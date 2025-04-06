from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn

class ProgressTracker:
    """Utility for tracking progress of long operations."""
    
    def __init__(self, description="Processing"):
        self.progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn()
        )
        self.task_id = None
        self.description = description
        
    def __enter__(self):
        self.progress.start()
        self.task_id = self.progress.add_task(f"[cyan]{self.description}", total=100)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.stop()
        
    def update(self, completed, total=None):
        """Update progress."""
        if total:
            self.progress.update(self.task_id, total=total)
        percentage = int(completed / total * 100) if total else completed
        self.progress.update(self.task_id, completed=percentage)
        
    def set_description(self, description):
        """Set a new description for the progress bar."""
        self.progress.update(self.task_id, description=f"[cyan]{description}") 
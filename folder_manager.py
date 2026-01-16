
import config

class FolderManager:
    def __init__(self, drive_service):
        self.drive_service = drive_service
        self.category_folders = {} # Cache implementation

    def get_target_folder_id(self, category):
        """
        Ensures the category folder exists in the root and returns its ID.
        """
        if category in self.category_folders:
            return self.category_folders[category]

        # Use dry run logic if needed, but for listing/existence checks we need real reads
        # Even in dry run, we might want to check if folder 'would' exist.
        # But simplify: try to find it.
        
        folder_id = self.drive_service.create_folder(category) 
        # Note: creates if not exists logic is inside drive_service.create_folder
        
        if folder_id:
            self.category_folders[category] = folder_id
            
        return folder_id

import os


def rename_folders(root_folder):
    for root, dirs, files in os.walk(root_folder, topdown=False):
        for dir_name in dirs:
            if ',' in dir_name:
                old_path = os.path.join(root, dir_name)
                new_name = dir_name.replace(',', '') 
                new_path = os.path.join(root, new_name)
                
                try:
                    os.rename(old_path, new_path)
                    print(f"Dossier renommé : {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Erreur lors du renommage de {old_path} : {e}")


if __name__ == "__main__":
    main_folder = "./dataset/"
    rename_folders(main_folder)
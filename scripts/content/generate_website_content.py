import os
import subprocess

def get_tree(path):
    try:
        result = subprocess.run(['tree', path], capture_output=True, text=True)
        return result.stdout
    except FileNotFoundError:
        # If 'tree' command is not available, use a simple directory listing
        tree = []
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * 4 * level
            tree.append(f'{indent}{os.path.basename(root)}/')
            for file in files:
                tree.append(f'{indent}    {file}')
        return '\n'.join(tree)

def get_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def main():
    # Set the specific path to your website directory
    website_dir = '/Users/Johared/Documents/Projects/marvinmtz-website'
    
    # Set the path for the output file
    output_dir = '/Users/Johared/Documents/Projects/marvinmtz-website/scripts/content'
    output_file = os.path.join(output_dir, 'marvinmtz-website.txt')
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as out_file:
        # Write the directory tree
        out_file.write("Directory Tree:\n")
        out_file.write(get_tree(website_dir))
        out_file.write("\n\n")
        
        # Walk through all files and directories
        for root, dirs, files in os.walk(website_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, website_dir)
                
                # Skip the output file itself
                if file == 'marvinmtz-website.txt':
                    continue
                
                # Write file name and path
                out_file.write(f"File: {relative_path}\n")
                out_file.write(f"Path: {file_path}\n")
                
                # Write file content for text-based files
                _, ext = os.path.splitext(file)
                if ext.lower() in ['.html', '.css', '.js', '.txt', '.md']:
                    out_file.write("Content:\n")
                    out_file.write(get_file_content(file_path))
                else:
                    out_file.write("(Binary file or unsupported format)")
                
                out_file.write("\n\n" + "="*50 + "\n\n")
    
    print(f"File created: {output_file}")

if __name__ == "__main__":
    main()

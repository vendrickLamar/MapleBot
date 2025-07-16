import os
import subprocess


# reads all the files in the /negative folder and generates neg.txt from them.
# we'll run it manually like this:
# $ python
# Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:21:23) [MSC v.1916 32 bit (Intel)] on win32
# Type "help", "copyright", "credits" or "license" for more information.
# >>> from cascade_utils import generate_negative_description_file
# >>> generate_negative_description_file()
# >>> exit()
def generate_negative_description_file():
    # open the output file for writing. will overwrite all existing data in there
    with open('monster_training/neg.txt', 'w') as f:
        # loop over all the filenames
        for filename in os.listdir('negative'):
            f.write('negative/' + filename + '\n')

# the opencv_annotation executable can be found in opencv/build/x64/vc15/bin
# generate positive description file using:
# $ C:\Users\afikm\Downloads\programs\opencv\opencv\build\x64\vc15\bin\opencv_annotation.exe --annotations=pos.txt --images=monster_training/positive/

# You click once to set the upper left corner, then again to set the lower right corner.
# Press 'c' to confirm.
# Or 'd' to undo the previous confirmation.
# When done, click 'n' to move to the next image.
# Press 'esc' to exit.
# Will exit automatically when you've annotated all of the images

# generate positive samples from the annotations to get a vector file using:
# C:\Users\afikm\Downloads\programs\opencv\opencv\build\x64\vc15\bin\opencv_createsamples.exe -info monster_training/pos.txt -w 24 -h 24 -num 1000 -vec pos.vec

# train the cascade classifier model using:
# C:\Users\afikm\Downloads\programs\opencv\opencv\build\x64\vc15\bin\opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -numPos 300 -numNeg 100 -numStages 12 -w 24 -h 24

# my final classifier training arguments:
# C:\Users\afikm\Downloads\programs\opencv\opencv\build\x64\vc15\bin\opencv_traincascade.exe -data monster_cascade/ -vec monster_training/pos.vec -bg monster_training/neg.txt -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos 133 -numNeg 300 -numStages 14 -w 24 -h 24 -maxFalseAlarmRate 0.4 -minHitRate 0.999

def generate_monster_vector_file():
    """
    Generates the pos.vec file for monster training using opencv_createsamples.exe.
    This function should be run before training the cascade classifier.
    """
    opencv_createsamples_path = r"C:\Users\afikm\Downloads\programs\opencv\opencv\build\x64\vc15\bin\opencv_createsamples.exe"
    original_pos_txt_path = "monster_training/pos.txt"
    temp_pos_txt_path = "temp_pos.txt"
    # Create the vector file in the current directory first, as shown in the example command
    pos_vec_path = "pos.vec"
    final_vec_path = "monster_training/pos.vec"

    # Get the current working directory for absolute paths
    current_dir = os.getcwd()

    try:
        # Create a temporary pos.txt file with absolute paths
        with open(original_pos_txt_path, 'r') as original_file:
            with open(temp_pos_txt_path, 'w') as temp_file:
                for line in original_file:
                    # Split the line into parts (first part is the image path, rest are coordinates)
                    parts = line.strip().split(' ')
                    if len(parts) > 1:
                        # Replace the relative path with an absolute path
                        image_path = parts[0]
                        # Remove the "monster_training/" prefix and convert to absolute path
                        if image_path.startswith("monster_training/"):
                            image_path = image_path[len("monster_training/"):]
                        # Create absolute path
                        abs_path = os.path.abspath(os.path.join("monster_training", image_path))
                        # Replace the path in the line
                        parts[0] = abs_path
                        # Join the parts back together
                        corrected_line = ' '.join(parts) + '\n'
                        temp_file.write(corrected_line)
                    else:
                        # If the line doesn't have coordinates (e.g., empty line), just write it as is
                        temp_file.write(line)

        # Command to create the vector file
        command = [
            opencv_createsamples_path,
            "-info", temp_pos_txt_path,
            "-w", "24",
            "-h", "24",
            "-num", "1000",
            "-vec", pos_vec_path
        ]

        print("Generating vector file for monster training...")
        print(" ".join(command))

        # Run the command
        subprocess.run(command, check=True)
        print(f"Vector file successfully created at {pos_vec_path}")

        # Move the file to the monster_training directory if needed
        import shutil
        if os.path.exists(pos_vec_path):
            # Create the monster_training directory if it doesn't exist
            os.makedirs(os.path.dirname(final_vec_path), exist_ok=True)
            # Move the file
            shutil.move(pos_vec_path, final_vec_path)
            print(f"Vector file moved to {final_vec_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating vector file: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_pos_txt_path):
            os.remove(temp_pos_txt_path)
            print(f"Temporary file {temp_pos_txt_path} removed")

from cascade_utils import generate_monster_vector_file

if __name__ == "__main__":
    print("Starting vector file generation...")
    generate_monster_vector_file()
    print("Vector file generation completed.")
    print("You can now run the cascade training command:")
    print(r"C:\Users\afikm\Downloads\programs\opencv\opencv\build\x64\vc15\bin\opencv_traincascade.exe -data monster_cascade/ -vec monster_training/pos.vec -bg monster_training/neg.txt -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos 133 -numNeg 300 -numStages 14 -w 24 -h 24 -maxFalseAlarmRate 0.4 -minHitRate 0.999")
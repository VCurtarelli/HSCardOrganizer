# HSCardOrganizer
Python script to automatically organize cards into folders and subfolders, by Class and Rarity.

## Step-by-Step

The script follows the following pipeline:
1. An image from `/unorg/` is opened ("target").
2. Rarity+type images are opened.
3. The script compares the target to each R+T image (through Euclidean distance), and selects the lowest distance as the correct.
4. Class images are opened (knowing the type and rarity).
5. The script compares the target to each Class image, and selects the lowest distance.
6. Knowing Class and Rarity, it moves the image to the correct folder (and creates if it doesn't exist).

Along that, there is another pipeline that happens above the previous one:
1. Finding the `/unorg/` folder.
2. Loading every filename that ends in ".png" from the folder.
3. Loading every folder from the `/unorg/` folder.
4. Execute the previous pipeline on each filename.
5. Execute the previous pipeline on a namelike file inside each folder.

## Usage

I recommend downloading the whole "CardOrganizer" folder. Cards to be organized must be put inside the `/unorg/` folder, and organized cards are put inside a `/00a Classes/` folder, parallel to the `/main/` and `/unorg/` ones. Any necessary folder will be created on the fly by the program, so you don't need to worry.

You'll need to have installed Python (v3.8 or newer), and the following Python packages:
- os
- shutil
- numpy
- skimage
- PIL

To run the script, you need to execute `main.py` inside the `/main/` folder, through the command line.

```python
cd "[YOUR_FOLDER]\HSCardOrganizer\main"
python main.py
```

## License

[GNU GPL v3.0](https://github.com/Artan0s/CardOrganizer/blob/main/LICENSE)

TL;DR: You can download, use, edit, and do almost anything. Just please, don't make a profit out of it.

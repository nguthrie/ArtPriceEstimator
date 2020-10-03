import os
path = r'C:\Users\Nicholas\Programming\ArtPriceEstimator\data'

top_folders = os.listdir(path)

train_dir = os.path.join(path, 'train')
# print(os.listdir(os.path.join(train_dir, '0-20')))
train_folders = []
[train_folders.append(os.path.join(train_dir, name)) for name in os.listdir(train_dir)]
print(train_folders)

[print(name[-6:], len(os.listdir(name))) for name in train_folders]

print()

test_dir = os.path.join(path, 'test')
# print(os.listdir(os.path.join(test_dir, '0-20')))
test_folders = []
[test_folders.append(os.path.join(test_dir, name)) for name in os.listdir(test_dir)]
print(test_folders)

[print(name[-6:], len(os.listdir(name))) for name in test_folders]
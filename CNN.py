import os
import shutil
from os import getcwd

import PIL
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd


# TO DO:
# copy the original pictures into training and testing
# get price and picture into a useable format
# set the CNN


def basic_analysis():
    cwd = getcwd()
    raw_images_path = os.path.join(cwd, 'images')  # don't need to use slashes, join does all the work
    # list with all image names
    image_names = os.listdir(raw_images_path)

    # change wd to images to start deleting
    os.chdir(raw_images_path)

    # transition table nonsense in python 3 - use regex in the future
    translation_table = dict.fromkeys(map(ord, ','), None)

    '''
    building new list of prices from image names.
    if image fails checks below, it's removed from list and deleted from directory
    if it passes, the image remains and the price is saved - this way the order of the
    price list and image list match
    '''
    prices = []
    for image_name in image_names:
        index = image_name.index('-')
        raw_price = image_name[index + 3:-5]
        no_comma = raw_price.translate(translation_table)
        price = float(no_comma)

        # need to check for images below size (100 x 100), or else error in datagen resizing
        image = PIL.Image.open(image_name)
        width, height = image.size
        image.close()

        # if price larger than 1000, remove image_name and delete the image from the local directory
        if price > 1000 or width < 100 or height < 100:
            print("removed: {}".format(image_name))
            image_names.remove(image_name)
            os.remove(image_name)
        else:
            prices.append(price)

    PricesDF = pd.Series(prices)
    print(PricesDF.describe())
    # print largest value for debugging purposes (have been manually removing inappropriate prices)
    # print(image_names[PricesDF.idxmax()])

    x_axis_values = range(0, len(PricesDF))
    y_axis_values = sorted(prices)
    plt.scatter(x_axis_values, y_axis_values, marker='.')
    plt.show()
    plt.boxplot(y_axis_values, notch=True, showfliers=False)
    plt.show()
    plt.hist(y_axis_values, bins=50)
    plt.show()

    return prices, image_names


# prices, image_names = basic_analysis()


# sanity checks on prices vs image_names
# print(len(prices), len(image_names))
# print(list(zip(prices, image_names))[:30])

def dataset_from_dl_folder(prices, image_names):
    """
    Take price list and image names list,
    split into train (80%) and test (20%) -> taking front 80% for train since randomized on alphabetical name save
    place the pictures into buckets
    buckets: 0-20, 20-60, 60-160, 160-300, 300-1000

    :return: None
    """

    split_index = round(len(prices) * .80)
    print(split_index)  # sanity check
    train_prices = prices[:split_index]
    test_prices = prices[split_index:]
    train_image_names = image_names[:split_index]
    test_image_names = image_names[split_index:]

    print(train_image_names)
    print(test_image_names)

    def sort_into_folders(prices, image_names, train_or_test):
        # train_or_test must be a string, which is used to create the path to the directory

        cwd = getcwd()
        for price, image_name in zip(prices, image_names):
            source_path = os.path.join(cwd, image_name)
            data_directory = os.path.join(r'C:\Users\Nicholas\Programming\ArtPriceEstimator\data', train_or_test)
            if price <= 20:
                dest_path = os.path.join(data_directory, '0-20')
                shutil.copy(source_path, dest_path)
            elif 20 < price <= 60:
                dest_path = os.path.join(data_directory, '20-60')
                shutil.copy(source_path, dest_path)
            elif 60 < price <= 160:
                dest_path = os.path.join(data_directory, '60-160')
                shutil.copy(source_path, dest_path)
            elif 160 < price <= 300:
                dest_path = os.path.join(data_directory, '160-300')
                shutil.copy(source_path, dest_path)
            elif 300 < price:
                print("Highest bucket:", price, image_name)
                dest_path = os.path.join(data_directory, '300-1000')
                shutil.copy(source_path, dest_path)



    sort_into_folders(train_prices, train_image_names, 'train')
    sort_into_folders(test_prices, test_image_names, 'test')


# dataset_from_dl_folder(prices, image_names)


def model():
    """
    Create and train the model.
    :return:
    """

    TRAINING_DIR = r"C:\Users\Nicholas\Programming\ArtPriceEstimator\data\train"
    training_datagen = ImageDataGenerator(
        # augmentation is used for reduce over-fitting - curious if I can get it to simply fit
        '''
        rescale=1. / 255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
        ''')

    VALIDATION_DIR = r'C:\Users\Nicholas\Programming\ArtPriceEstimator\data\train'
    validation_datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = training_datagen.flow_from_directory(
        TRAINING_DIR,
        target_size=(100, 100),
        class_mode='categorical',
        batch_size=1
    )

    validation_generator = validation_datagen.flow_from_directory(
        VALIDATION_DIR,
        target_size=(100, 100),
        class_mode='categorical',
        batch_size=1
    )

    model = tf.keras.models.Sequential([
        # Note the input shape is the desired size of the image 150x150 with 3 bytes color
        # This is the first convolution
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(100, 100, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        # The second convolution
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        # The third convolution
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        # The fourth convolution
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        # Flatten the results to feed into a DNN
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.5),
        # 512 neuron hidden layer
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(5, activation='softmax')
    ])

    model.summary()

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    history = model.fit(train_generator, epochs=20, validation_data=validation_generator, verbose=1)

    model.save("rps.h5")

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(len(acc))

    plt.plot(epochs, acc, 'r', label='Training accuracy')
    plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.legend(loc=0)
    plt.figure()

    plt.plot(epochs, loss, 'bo', label='Training Loss')
    plt.plot(epochs, val_loss, 'b', label='Validation Loss')
    plt.title('Training and validation loss')
    plt.legend()

    plt.show()

model()

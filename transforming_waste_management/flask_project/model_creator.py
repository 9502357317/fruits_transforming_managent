import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import os

def create_healthy_vs_rotten_model():
    """
    Creates a CNN model for healthy vs rotten fruit classification
    """
    print("Creating healthy vs rotten classification model...")
    
    # Model Architecture
    model = keras.Sequential([
        # Input layer
        layers.Input(shape=(224, 224, 3)),
        
        # Data augmentation layers
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
        
        # Rescaling
        layers.Rescaling(1./255),
        
        # Convolutional layers
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(128, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(256, 3, activation='relu'),
        layers.MaxPooling2D(),
        
        # Flatten and dense layers
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu'),
        layers.Dense(1, activation='sigmoid')  # Binary classification
    ])
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def create_vgg16_transfer_model():
    """
    Creates a model using VGG16 transfer learning
    """
    print("Creating VGG16 transfer learning model...")
    
    # Load pre-trained VGG16 model
    base_model = tf.keras.applications.VGG16(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )
    
    # Freeze base model layers
    base_model.trainable = False
    
    # Add custom classifier
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(1, activation='sigmoid')
    ])
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def create_simple_model():
    """
    Creates a simple model for testing purposes
    """
    print("Creating simple test model...")
    
    model = keras.Sequential([
        layers.Input(shape=(224, 224, 3)),
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_with_dummy_data(model, epochs=5):
    """
    Train model with dummy data for testing
    """
    print("Training model with dummy data...")
    
    # Create dummy training data
    X_train = np.random.rand(100, 224, 224, 3)
    y_train = np.random.randint(0, 2, 100)
    
    # Create dummy validation data
    X_val = np.random.rand(20, 224, 224, 3)
    y_val = np.random.randint(0, 2, 20)
    
    # Train model
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=16,
        verbose=1
    )
    
    return history

def main():
    """
    Main function to create and save the model
    """
    print("Starting model creation process...")
    
    # Choose model type
    model_type = input("Choose model type (1: Simple, 2: CNN, 3: VGG16): ").strip()
    
    if model_type == "1":
        model = create_simple_model()
    elif model_type == "2":
        model = create_healthy_vs_rotten_model()
    elif model_type == "3":
        model = create_vgg16_transfer_model()
    else:
        print("Invalid choice. Creating simple model...")
        model = create_simple_model()
    
    # Display model summary
    print("\nModel Summary:")
    model.summary()
    
    # Ask if user wants to train with dummy data
    train_choice = input("\nTrain with dummy data? (y/n): ").strip().lower()
    
    if train_choice == 'y':
        epochs = int(input("Enter number of epochs (default 5): ") or 5)
        train_with_dummy_data(model, epochs)
    
    # Save model
    model.save('healthy_vs_rotten.h5')
    print("\nModel saved as 'healthy_vs_rotten.h5'")
    print("You can now run your Flask application!")

if __name__ == "__main__":
    main()
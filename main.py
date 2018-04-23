import vgg16
import load_dataset_simulator
import load_dataset_spurv
import save_load_model
import heat_map
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
import pickle

def main():

    print("Creating model...")
    vgg16.vgg16()

    print("Loading model...")
    #model = load_model("vgg16_test.h5")
    #model = load_model("trained_model_simulator.h5")
    model = load_model("model-010.h5")

    checkpoint = ModelCheckpoint('model-{epoch:03d}.h5', monitor='val_loss',verbose=0,save_best_only=True, mode='auto') #Saved_models/

    np_val_images, np_val_steering = load_dataset_simulator.load_dataset("center","test")

    for dataset in ["LEFT", "RIGHT", "mond", "mond2", "mond3", "mond4"]:
        for camera_angle in ["center", "right", "left"]:
            print("Currently training on dataset: ", dataset, ", angle: ", camera_angle, ".")
            np_images, np_steering = load_dataset_simulator.load_dataset(camera_angle,dataset)
            history = model.fit(x=np_images, y=np_steering, epochs=10, batch_size=5, callbacks=[checkpoint], validation_data=(np_val_images, np_val_steering))
            #print("Saving the model...")
            #save_load_model.save_model(model, "trained_model_simulator")

    print("Saving the model...")
    save_load_model.save_model(model, "trained_model_simulator")

    print("Creating heatmap...")
    heat_map.heat_map()

    with open('history1.txt', 'wb') as file_pi: #Saved_history/
        pickle.dump(history.history, file_pi)

    print("Finished!")

    return 0;


if __name__== "__main__":
    main()

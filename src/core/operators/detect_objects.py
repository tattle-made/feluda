def initialize(param):
    from ultralytics import YOLO

    global output_directory
    output_directory = r"sample_data/yolo_output"

    global model
    model = YOLO("yolov8n-seg.pt")
    print("model successfully downloaded")


def count_objects(predictions, target_classes):
    object_counts = {x: 0 for x in target_classes}
    for prediction in predictions:
        for c in prediction.boxes.cls:
            c = int(c)
            if c in target_classes:
                object_counts[c] += 1
            elif c not in target_classes:
                object_counts[c] = 1

    present_objects = object_counts.copy()

    for i in object_counts:
        if object_counts[i] < 1:
            present_objects.pop(i)

    return present_objects


def run(image_path):
    lables = []
    result = model.predict(
        image_path,
        save=True,
        imgsz=1024,
        conf=0.5,
        project="sample_data",
        name="output",
    )

    names = model.names
    for r in result:
        for c in r.boxes.cls:
            # print(names[int(c)])
            lables.append(names[int(c)])
    # count_objects_num = count_objects(result, names)
    # print(count_objects_num)

    return result, lables


def cleanup(param):
    pass


def state():
    pass


# if __name__ == "__main__":
#     class_names = []
#     initialize(param={})
#     image_path = r'sample_data/people.jpg'
#     detect_objects, class_names = run(image_path)
#     print(class_names)

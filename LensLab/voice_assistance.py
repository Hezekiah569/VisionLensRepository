import pyttsx3


def provide_voice_feedback(detected_objects, class_names):
    engine = pyttsx3.init()

    # Get available voices
    voices = engine.getProperty('voices')

    # Set the engine to use a female voice (typically index 1 is female)
    engine.setProperty('voice', voices[1].id)  # 0 is usually male, 1 is usually female

    if detected_objects:
        object_names = []
        for obj in detected_objects:
            if 'class' in obj and 'confidence' in obj:  # Ensure both keys are present
                index = obj['class']  # Class index
                confidence = obj['confidence']  # Confidence score

                if 0 <= index < len(class_names) and confidence >= 0.5:  # Check for valid index and confidence
                    object_names.append(class_names[index])

        feedback = f"There's a {', and a '.join(object_names)}" if object_names else "I don't see anything recognizable."
    else:
        feedback = "No objects detected."

    print(detected_objects)
    engine.say(feedback)
    engine.runAndWait()

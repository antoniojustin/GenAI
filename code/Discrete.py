import openai
import pandas as pd
import os
import base64

# Input the paths for both images and texts:
code_book_path = "Code Book.xlsx"
df = pd.read_excel(code_book_path)
image_folder = "Processed_Frames/"

# Helper function to encode the image to base64 format
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Set your OpenAI API Key
OpenAi_api =
Grok2_api =
DeepSeek_api =

# Function to get the emotion classification from OpenAI API
def classify_emotion_with_LLM(image_path, caption, LLM):
    """
    Uses the specified LLM to classify emotions based on image and caption together.
    """
    if LLM.lower() == "gpt-4o":
        client = openai.OpenAI(api_key=OpenAi_api)
        model_name = "gpt-4o"

    elif LLM.lower().startswith("grok"):
        client = openai.OpenAI(api_key=Grok2_api, base_url="https://api.x.ai/v1")
        model_name = "grok-2-vision-1212"

    elif LLM.lower().startswith("deepseek"):
        client = openai.OpenAI(api_key=DeepSeek_api, base_url="https://api.deepseek.com")
        model_name = "deepseek-chat"

    system_message = {
        "role": "system",
        "content": (
            "You are an expert in emotion classification. "
            "You will be given an image (optional) and a corresponding caption (verbal cues). "
            "Classify the primary emotion into one of the following categories: "
            "(1) happy, (2) sad, (3) anger, (4) fear, (5) surprise, (6) disgust, (7) neutral. "
            "Respond with only one word."
        )
    }

    # General Text User Message
    user_message = [{"type": "text", "text": f"Caption: {caption}"}]

    if LLM.lower() == "gpt-4o":  # DeepSeek does not support images
        image_base64 = encode_image(image_path)
        user_message.append({"type": "image_url",
                             "image_url": {
                                 "url": f"data:image/jpeg;base64, {image_base64}"}})

    # Call OpenAI's Chat API with image + text
    response = client.chat.completions.create(
        model=model_name,
        messages=[system_message, {"role": "user", "content": user_message}],
        max_tokens=100,
        temperature=0.7
    )

    # Extract the predicted emotion
    predicted_emotion = response.choices[0].message.content.strip()
    return predicted_emotion

# Loop through each row in the DataFrame and classify the emotion
results = []
for index, row in df.iterrows():
    image_name = row["frame_id"]
    caption = row["caption"]

    # Ensure the image exists in the processed_Frames folder
    # Append ".jpg" to match actual filenames
    image_filename = f"{image_name}.jpg"
    image_path = os.path.join(image_folder, image_filename)
    if not os.path.exists(image_path):
        print(f"Warning: Image {image_path} not found!")
        continue

    # Convert image to base64 format
    image_base64 = encode_image(image_path)

    # Get the predicted emotion from GPT-4o
    chatgpt_classification = classify_emotion_with_LLM(image_path, caption,
                                                    LLM="gpt-4o")
    grok_classification = classify_emotion_with_LLM(image_path, caption,
                                                 LLM="grok-2-latest")
    deepseek_classification = classify_emotion_with_LLM(image_path, caption,
                                                     LLM="deepseek-chat")

    # Store the results
    results.append({
        "image_name": image_filename,
        "caption": caption,
        "chatgpt_classification": chatgpt_classification,
        "grok_classification": grok_classification,
        "deepseek_classification": deepseek_classification
    })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save the results to a CSV file
results_df.to_csv("emotion_analysis_results_with_all_LLMs.csv", index=False)
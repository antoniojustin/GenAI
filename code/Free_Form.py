# second task to get a free form answer
def classify_emotion_with_explanation(image_base64, caption):
    """
    Uses GPT-4o to analyze emotions based on an image and caption together, providing a short paragraph explanation.
    """
    system_message = {
        "role": "system",
        "content": (
            "Based on the given verbal and non-verbal cues, "
            "determine the primary emotion of the individuals."
            "Explain why in a short paragraph"
        )
    }

    user_message = {
        "role": "user",
        "content": [
            {"type": "text", "text": f"Caption: {caption}"},
            {"type": "image_url",
             "image_url": {
                 "url": f"data:image/jpeg;base64, {image_base64}"}}
        ]
    }

    # Call OpenAI's Chat API with image + text
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[system_message, user_message],
        max_tokens=100,  # Allowing more tokens for a paragraph response
        temperature=0.7
    )

    # Extract the generated explanation
    explanation = response.choices[0].message.content.strip()
    return explanation

# Loop through each row in the DataFrame and analyze the emotion with explanation
results = []
for index, row in df.iterrows():
    image_number = str(row["frame_id"])  # Convert number to string
    caption = row["caption"]

    # Construct the image file path
    image_filename = f"{image_number}.jpg"
    image_path = os.path.join(image_folder, image_filename)

    # Ensure the image exists in the processed_Frames folder
    if not os.path.exists(image_path):
        print(f"Warning: Image {image_path} not found!")
        continue

    # Convert image to base64 format
    image_base64 = encode_image(image_path)

    # Get the explanation from GPT-4o
    explanation = classify_emotion_with_explanation(image_base64, caption)

    # Store the results
    results.append({
        "image_name": image_filename,
        "caption": caption,
        "emotion_explanation": explanation
    })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save the results to a CSV file
results_df.to_csv("emotion_analysis_results_with_explanations.csv", index=False)
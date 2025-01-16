import cv2
import webbrowser
from pyzbar.pyzbar import decode

def handle_qr_data(data):
    """Perform actions based on the QR code data."""
    print(f"Processing QR code data: {data}")
    
    # Example: Open a URL if the data is a web address
    if data.startswith("http://") or data.startswith("https://"):
        print("Opening URL in the browser...")
        webbrowser.open(data)
    else:
        print(f"No specific action defined for: {data}")

def scan_qr_code():
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # Use 0 for default camera

    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    print("QR Code Scanner started. Press 'q' to quit.")
    
    processed_codes = set()  # Store processed QR codes to avoid duplicates
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Detect and decode QR codes
        qr_codes = decode(frame)

        for qr in qr_codes:
            # Get QR data and type
            qr_data = qr.data.decode('utf-8')

            # Check if QR code was already processed
            if qr_data not in processed_codes:
                processed_codes.add(qr_data)  # Mark the QR code as processed
                qr_type = qr.type

                # Draw bounding box
                x, y, w, h = qr.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Display QR data on the frame
                text = f"{qr_type}: {qr_data}"
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # Print and handle QR data
                print(f"Detected QR Code: {qr_data}")
                handle_qr_data(qr_data)

                # Wait before processing next QR code to avoid multiple openings of same URL
                cv2.waitKey(500)  # Wait for half a second to allow for one scan per QR code

        # Show the video feed with detected QR codes
        cv2.imshow("QR Code Scanner", frame)

        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_qr_code()

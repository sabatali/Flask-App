# from app import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)

import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv("PORT", 10000))  # Get Render's assigned port
    print(f"Running on port {port}")  # Debugging log
    app.run(host="0.0.0.0", port=port, debug=True)  # Bind to 0.0.0.0

## Rest API: 2nd Product API

![GitHub](https://img.shields.io/github/license/Prathameshdhande22/2nd-Product-API?logo=github&color=blue&style=flat-square)

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

**Description:**  
2nd Product API is a RESTful API similar to the OLX website. Users can register and login to obtain an access token, enabling them to explore the API, sell products, buy items, and add products to their cart. The API provides powerful search capabilities, allowing users to find products based on queries, tags, or view all available products.

**Made with:**  
- Python
- FastAPI
- Pydantic Models
- Mongoengine

**API Documentation:**  
[https://twondproductapi.onrender.com](https://twondproductapi.onrender.com)

**License:**  
This project is licensed under the MIT License. [License File](LICENSE)

**API Link:**  
[https://twondproductapi.onrender.com/](https://twondproductapi.onrender.com/)

**Running the API Locally:**  
1. Clone the repository: 
```
git clone https://github.com/PrathameshDhande22/2nd-Product-API.git
```
2. Create a virtual environment: 
```
python -m venv venv
```

3. Activate the virtual environment:
   - On Windows: 
   ```
   venv\Scripts\activate
   ```
   - On macOS and Linux: 
   ```
   source venv/bin/activate
   ```
4. Install dependencies: 
```
pip install -r reqirements.txt
```
5. Edit `.env` file:
```
MONGODB_URI="Your MongoDB URI"
SECRET_KEY="Your Secret Key"
```

5. Run the `run.py` 
file: 
```
python run.py
```

## Author : Prathamesh Dhande
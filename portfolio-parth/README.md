# Parth Patel - Senior Data Engineer Portfolio

A professional portfolio website showcasing my experience as a Senior Data Engineer with expertise in Azure, Databricks, PySpark, and modern data engineering practices.

## Features

- Professional portfolio with experience timeline
- Skills and expertise showcase
- Contact information and resume download
- Blog integration
- Responsive design with Bootstrap

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLAlchemy
- **Authentication**: Flask-JWT-Extended
- **Deployment**: Python WSGI

## Quick Start

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd portfolio
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory:
```
JWT_SECRET_KEY=your-secret-key-here
```

5. Run the application:
```bash
python run.py
```

The application will be available at `http://localhost:5899`

## Project Structure

```
portfolio/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── core/                # Main portfolio routes and templates
│   ├── dashboard/           # Admin dashboard (if needed)
│   ├── blogs/               # Blog functionality
│   ├── model/               # Database models
│   └── static/              # Static assets (CSS, JS, images)
├── resume/                  # Resume files
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Contact

- **Email**: pparth967@gmail.com
- **Phone**: 519-778-5965
- **LinkedIn**: [Parth Patel](https://www.linkedin.com/in/parth-patel-72a92611a/)
- **GitHub**: [parth967](https://github.com/parth967)

## License

This project is for portfolio purposes. All rights reserved.
# codekijiji.ai

This project is part of the initiative to develop a Language Learning Model (LLM) for Kenyan indigenous languages, focusing on the Kikuyu language. It includes a web-based data collection interface for public text and voice submissions.

## Development

This project was developed using React and Chakra UI for a responsive and accessible user interface. Contributions to the project are managed via GitHub and continuous integration/deployment. Recent updates include the integration of a Google Form for partnership inquiries and enhancements to the data analysis script for improved visualization.

## Running the Project Locally

To run this project locally:

1. Clone the repository.
2. Navigate to the project directory.
3. Run `npm install` to install dependencies.
4. Run `npm start` to start the development server.
5. Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

## Data Analysis and Visualization

The project includes a Python script `data_analysis_template.py` for data analysis and visualization. This script uses Plotly to generate interactive visualizations, which can be embedded into the React application for enhanced data insights. To run the data analysis script:

1. Ensure you have Python and the necessary libraries installed.
2. Navigate to the `frontend_build` directory.
3. Run `python data_analysis_template.py` to execute the script and generate visualizations.

## Testing

To ensure the reliability and user-friendliness of the application, a comprehensive test suite has been developed. This includes unit tests for the React components and integration tests for the AWS services. To run the tests:

1. Navigate to the `frontend_build` directory.
2. Run `npm test` to execute the test suite.

Please note that any new features should be accompanied by corresponding tests to maintain the quality and stability of the application.

## Contributing

We welcome contributions to the `codekiijiji.ai` project. Please read our contributing guidelines before submitting a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

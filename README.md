# Gender Inequality InfoViz

This project visualizes gender inequality metrics across countries and time using map plots and bubble charts. The data is sourced from the World Bank's Gender Portal, which compiles information from UN, UN Women, UNICEF, and other premier sources. The data is divided into two categories: **Societal Metrics** (education, economic, and political involvement of women) and **Maternal Healthcare** (maternal/child death rates, access to healthcare).

## Dependencies

This project requires the following Python libraries:
- **Streamlit**: For interactive web visualization
- **Plotly**: For generating charts and maps
- **Pandas**: For data handling

You can install these dependencies using pip:

```bash
pip install streamlit plotly pandas
```

## Files
```utils.py```: Contains the functions utilized in the visualization generation.
```visualization.py```: Contains the main code for visualization itself.
```compiled_data.csv```: Contains a compilation of time and country-wise data for different metrics of gender inequality.

## How to use
1. Import necessary libraries. (See Dependencies above)
2. Open the terminal in your Python IDE and run command:
   ```streamlit run visualization.py```
4. Ensure that you are in the correct directory where the files are located.

## Notes
You can use the functions in ```utils.py``` to visualize any CSV data, as long as it is structured with two main dimensions (like time and country in this case), and contains metrics along a single axis.

## References
- World Bank Gender Data Portal. Retrieved from [https://genderdata.worldbank.org/en/topics](https://genderdata.worldbank.org/en/topics)



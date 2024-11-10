import plotly.express as px
import pandas as pd
import streamlit as st
from itertools import product


def prepare_plotly_data(csv_path):
    df = pd.read_csv(csv_path)
    # Ensure that the DataFrame is sorted by Year and reset the index
    df = df.sort_values(by="Year").reset_index(drop=True)

    # Get unique years and regions
    years = df['Year'].unique()
    regions = df['Region'].unique()

    # Create a MultiIndex of all combinations of years and regions
    full_index = pd.MultiIndex.from_product([years, regions], names=['Year', 'Region'])
    df_full = pd.DataFrame(index=full_index).reset_index()

    # Merge the original data with the full index to ensure every region has data for each year
    df = pd.merge(df_full, df, on=["Year", "Region"], how="left")

    return df


def create_choropleth(df, metric, color_scale, animation_speed, title, color_range=None, height=450, time_var="Year",
                      unit_var="Country Code", unit_label="Country Name"):

    if color_range is None:
        color_range = [df[metric].min(), df[metric].max()]

    fig = px.choropleth(
        df,
        locations=unit_var,
        color=metric,
        animation_frame=time_var,
        hover_name=unit_label,
        hover_data={unit_label: False, unit_var: False, time_var: True, metric: True},
        color_continuous_scale=color_scale,
        labels={metric: ""},
        title=title
    )
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = animation_speed
    fig.update_geos(showcoastlines=True, coastlinecolor="LightGray")
    fig.update_layout(
        coloraxis=dict(cmin=color_range[0], cmax=color_range[1]),
        coloraxis_colorbar=dict(title=None),
        height=height,
        margin=dict(l=0, r=0, t=40, b=40)
    )
    return fig


class MetricBubbleMapPlots:
    def __init__(
            self,
            df,
            animation_speed=200,
            default_size=2.5,
            time_var="Year",
            unit_var="Country Code",
            class_var="Region",
            x_var="Women with Secondary Education (%)",
            y_var="Labor, Women in Industry & Services (%)",
            z_var="Legislative Representation (%)",
            unit_label="Country Name",
            x_label="% of Women aged 15+ with at least Secondary Education",
            y_label="% of total Labor Force: Women aged 15+ in Industry & Services",
            z_label="% of legislative seats for Women",
            title="Women's Educational, Economic & Political Representation",
            x_range=[0, 100],
            y_range=[0, 60],
            z_range=[0, 100],
            plot_height=900,
            map_height=450
    ):
        self.df = df
        self.animation_speed = animation_speed
        self.default_size = default_size
        self.time_var = time_var
        self.unit_var = unit_var
        self.class_var = class_var
        self.x_var = x_var
        self.y_var = y_var
        self.z_var = z_var
        self.unit_label = unit_label
        self.x_label = x_label
        self.y_label = y_label
        self.z_label = z_label
        self.title = title
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range
        self.plot_height = plot_height
        self.map_height = map_height

    def bubble_chart(self):
        df = self.df.copy()
        df['Size'] = df[self.z_var].apply(lambda x: self.default_size if pd.isna(x) or x == 0 else x)

        hover_data = {
            "Size": False,
            self.x_var: ':.2f',
            self.y_var: ':.2f',
            self.z_var: ':.2f'
        }

        fig = px.scatter(
            df,
            x=self.x_var,
            y=self.y_var,
            animation_frame=self.time_var,
            animation_group=self.unit_var,
            size="Size",
            color=self.class_var,
            hover_name=self.unit_label,
            labels={
                self.x_var: self.x_var,
                self.y_var: self.y_var,
                self.z_var: self.z_var
            },
            title=self.title,
            template="plotly_white",
            hover_data=hover_data  # Customize hover data
        )

        # Set animation speed
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = self.animation_speed

        # Dynamic axis range if not provided
        if self.x_range is None:
            self.x_range = [df[self.x_var].min() - 5, df[self.x_var].max() + 5]
        if self.y_range is None:
            self.y_range = [df[self.y_var].min() - 5, df[self.y_var].max() + 5]

        # Set the axis ranges and other layout options
        fig.update_layout(
            xaxis_title=self.x_label,
            yaxis_title=self.y_label,
            legend_title=self.class_var,
            xaxis=dict(range=self.x_range),
            yaxis=dict(range=self.y_range),
            coloraxis_colorbar=dict(title="Region"),
            height=self.plot_height,
            margin=dict(l=0, r=0, t=40, b=40)
        )

        return fig

    def map_plots(self):
        plot1 = create_choropleth(self.df, self.x_var, color_scale="Blues", animation_speed=self.animation_speed,
                                  title=self.x_label, color_range=self.x_range, height=self.map_height,
                                  time_var=self.time_var, unit_var=self.unit_var, unit_label=self.unit_label)
        plot2 = create_choropleth(self.df, self.y_var, color_scale="Purples", animation_speed=self.animation_speed,
                                  title=self.y_label, color_range=self.y_range, height=self.map_height,
                                  time_var=self.time_var, unit_var=self.unit_var, unit_label=self.unit_label)
        plot3 = create_choropleth(self.df, self.z_var, color_scale="Greens", animation_speed=self.animation_speed,
                                  title=self.z_label, color_range=self.z_range, height=self.map_height,
                                  time_var=self.time_var, unit_var=self.unit_var, unit_label=self.unit_label)

        return plot1, plot2, plot3

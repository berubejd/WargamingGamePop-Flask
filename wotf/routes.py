import pygal

from collections import defaultdict
from datetime import datetime
from datetime import timedelta

from flask import Blueprint, current_app as app, render_template, url_for
from pygal.style import Style

from . import create_app
from . import db
from .models import Population_Data


main_bp = Blueprint(
    "routes", __name__, template_folder="templates", static_folder="static"
)


@main_bp.route("/", methods=["GET"])
def index():
    # SVG rendering fails with too many datapoints so reduced to hourly over 24 hours
    search_time = datetime.utcnow() - timedelta(hours=24)
    pop_dict = defaultdict(list)
    labels = []
    labels_major = []

    # pop_datapoints = Population_Data.query.filter(Population_Data.timestamp > search_time).all()

    pop_datapoints = (
        Population_Data.query.filter(Population_Data.timestamp > search_time)
        # .filter(db.extract("minute", Population_Data.timestamp).in_([0, 15 ,30, 45]))
        .filter(db.extract("minute", Population_Data.timestamp) == 0).all()
    )

    if pop_datapoints:
        for dp in pop_datapoints:
            pop_dict[dp.region].append(dp.count)

            if not dp.timestamp in labels:
                labels.append(dp.timestamp)

            if (
                dp.timestamp.minute == 30 or dp.timestamp.minute == 0
            ) and not dp.timestamp in labels_major:
                labels_major.append(dp.timestamp)

    else:
        data = None

    # Create chart style
    custom_style = Style(
        font_family="Segoe UI",
        title_font_size=32,
        background="transparent",
        plot_background="transparent",
        foreground="#999",
        foreground_strong="#eee",
        foreground_subtle="#555",
        opacity=".1",
        opacity_hover=".75",
        transition="1s ease-out",
        colors=(
            "#ff5995",
            "#b6e354",
            "#feed6c",
            "#8cedff",
            "#9e6ffe",
            "#899ca1",
            "#f8f8f2",
            "#bf4646",
            "#516083",
            "#f92672",
            "#82b414",
            "#fd971f",
            "#56c2d6",
            "#808384",
            "#8c54fe",
            "#465457",
        ),
    )

    # Set up chart
    chart = pygal.StackedLine(
        width=900,
        height=600,
        fill=True,
        interpolate="cubic",
        style=custom_style,
        show_minor_x_labels=False,
    )

    chart.title = "World of Tanks Worldwide Population"

    # Add population data
    if pop_dict:

        for region, data in pop_dict.items():
            chart.add(region, data)

        chart.x_labels = labels
        chart.x_labels_major = labels_major

    else:
        chart.add("No Data", [])

    chart = chart.render_data_uri()

    return render_template("index.html", chart=chart)

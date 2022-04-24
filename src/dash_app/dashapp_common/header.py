from pydoc import classname
from dash import html


layout = html.Div(
    className = "bg-light m-3 p-3",
    children = [
        html.A(
            className = "fs-2 fw-bold link-dark",
            href="/",
            children= [ 
                html.Img(src='assets/cms_logo.png', height='50', width='50', className="d-inline-block align-text-bottom"),
                " CMS Rucio Data Dashboard"
            ],    
        ),
        html.Div(className="lead", children=["Monitoring for data in Rucio Managed RSEs"])
    ]
)



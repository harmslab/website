#!/usr/bin/env python
__description__ = \
"""
Install the website into the github docs folder (like sphinx-build)
"""
__author__ = "Michael J. Harrms"
__usage__ = "build.py source_dir [target_dir]"

import jinja2
import mistune

import pandas as pd
import numpy as np

import sys, os, re, glob, shutil

def generate_hover(image_file,
                   text=None,
                   link=None,
                   html=None,
                   text_class=None,
                   image_class=None,
                   alt_text=None):
    """
    Generate html that encodes hovering-over image effects.

    image_file: an image file (required)
    text: text to show on hover
    link: link when image is clicked on
    html: html to show when image is clicked on (placed after text)
    text_class: class to assign text
    image_class: class to assign image
    alt_text: alt_text to show if image is missing
    """

    # Make sure file exists
    if not os.path.isfile(image_file):
        err = f"Image file ({image_file}) does not exist.\n"
        raise FileNotFoundError(err)

    # Get text class
    if text_class is None:
        text_class = "hover-text"
    else:
        text_class = f"hover-text {text_class}"

    # Get image class
    if image_class is None:
        image_class = "hover-image"
    else:
        text_class = f"hover-text {image_class}"

    # Get alt-text
    if alt_text is None:
        alt_text = "image"

    # Create hover-holder div
    out = []
    out.append(f"<div class=\"hover-holder\" >")

    # Add link
    if link is not None:
        out.append(f"<a href=\"{link}\">")

    # Create image and overlay classes
    out.append(f"<img src=\"{image_file}\" alt=\"{alt_text}\" class=\"{image_class}\">")
    out.append(f"<div class=\"hover-overlay\">")
    if text is not None:
        out.append(f"<div class=\"{text_class}\">{text}</div>")
    if html is not None:
        out.append(html)
    out.append("</div>")

    # Close link
    if link is not None:
        out.append("</a>")

    # Close div
    out.append("</div>")

    return "".join(out)

def to_projects(df,col_per_row=4):
    """
    Parse "projects" tab from spreadsheet and generate pretty rows.

    df: dataframe extracted from spreadsheet.
    col_per_row: number of columns per row.
    """

    # Break projects into rows
    out = []
    for i in range(len(df)):
        if i % col_per_row == 0:
            out.append([])

        row = df.iloc[i,:]
        out[-1].append({"title":row["title"],
                        "img":"img/fig/{}".format(row["img"]),
                        "link":row["link"]})

    html = []
    col_div = "<div class=\"col-xl-4 col-md-6 col-xs-12 mt-2 mb-3\">"

    html.append("<div class=\"row\">")
    for row in out:

        for i in range(len(row)):
            img = row[i]["img"]
            title = row[i]["title"]
            link = row[i]["link"]

            html.append(col_div)
            html.append(generate_hover(img,text=title,link=link,text_class="fund-text"))
            html.append("</div>")


    html.append("</div>")
    html.append("<br/>")

    return "".join(html)


def to_people(df,col_per_row=6):
    """
    Generate html holding lab members given an input data frame with
    name, title, description, img, github, twitter, email, website,
    and linkedin for each user.
    """

    # Break people into rows
    out = []
    for i in range(len(df)):
        if i % col_per_row == 0:
            out.append([])

        row = df.iloc[i,:]
        name = row["name"]
        name = "<br/>".join(name.split())
        title = row["title"]
        desc = row["description"]
        img = "img/headshots/{}".format(row["img"])

        # Remove empty descriptions
        try:
            if np.isnan(desc):
                desc = ""
        except TypeError:
            pass


        links = []
        for possible in ["github","twitter","email","website","linkedin"]:

            try:
                if np.isnan(row[possible]):
                    continue
            except TypeError:
                l = row[possible].strip()
                icon = "img/icons/{}.png".format(possible)
                links.append(f"<a href=\"{l}\" class=\"btn btn-link p-0\"><img src=\"{icon}\" class=\"\" alt=\"{possible}\"></a>")


        dummy_img = "<img src=\"img/icons/dummy.png\" class=\"\" alt=\"dummy\">"

        if len(links) == 4:
            links.append(dummy_img)
        elif len(links) == 3:
            links.insert(0,dummy_img)
            links.append(dummy_img)
        elif len(links) == 2:
            links.insert(0,dummy_img)
            links.append(2*dummy_img)
        elif len(links) == 1:
            links.insert(0,2*dummy_img)
            links.append(2*dummy_img)
        elif len(links) == 0:
            links.insert(0,dummy_img*5)
        else:
            continue

        link_group = "<div class=\"btn-group\" role=\"group\" style=\"width:100%\">"
        links.insert(0,link_group)
        links.append("</div>")

        out[-1].append({"name":name,
                        "title":title,
                        "desc":desc,
                        "img":img,
                        "links":"".join(links)})


    html = []
    col_div = " <div class=\"col-lg-2 col-sm-3 col-xs-12 p-1\">"
    sub_row_string = "<div class=\"row\">{:}</div>"

    html.append("<div class=\"row\">")
    for row in out:


        for i in range(len(row)):

            this_row = []
            img = row[i]["img"]
            name = row[i]["name"]
            title = row[i]["title"]
            links = row[i]["links"]
            desc = row[i]["desc"]

            # Create column
            this_row.append(col_div)

            # Create card
            this_row.append("<div class=\"card m-0\" style=\"height:100%\">")

            # Create card image top
            this_row.append(f"<img src=\"{img}\" class=\"card-img-top person-img p-2\">")

            # Create card body
            this_row.append("<div class=\"card-body m-0 p-0 \">")
            this_row.append(f"<h4 class=\"card-title person-name\">{name}</h4>")
            this_row.append(f"<h5 class=\"card-subtitle person-title\">{title}</h5>")
            this_row.append(f"<br/><p class=\"card-text person-desc\">{desc}</p><br/>")
            this_row.append("</div>")

            # Create card footer
            this_row.append("<div class=\"card-footer m-0 p-0\">")
            this_row.append(f"<p class=\"card-text person-links\">{links}</p>")
            this_row.append("</div>")

            this_row.append("</div>")

            # Close column
            this_row.append("</div>")

            html.append("".join(this_row))

    html.append("</div>")
    html.append("<br/>")

    return "".join(html)

def to_publications(df,main_author="Harms MJ"):
    """
    Generate pretty publications list.
    """

    p = re.compile(main_author)

    html = ["<div class=\"list-group\">"]
    for i in range(len(df.year))[::-1]:
        row = df.iloc[i,:]

        authors = row.authors
        authors = p.sub(f"<span class=\"publication-main-author\">{main_author}</span>",authors)
        authors = f"<span class=\"publication-authors\">{authors}</span>"

        title = row.title
        title = f"<span class=\"publication-title\">{title}</span>"

        if row.status == "published":
            year = row.year
        else:
            year = row.status
        year = f"<span class=\"publication-year align-left\">{year}</span>"

        journal = row.journal
        journal = f"<span class=\"publication-journal\">{journal}</span>"

        link = row.link
        try:
            if np.isnan(link):
                link = ""
        except TypeError:
            pass

        meta = row.meta
        try:
            if np.isnan(meta):
                meta = ""
        except TypeError:
            pass

        meta = f"<span \class=\"publication-meta\">{meta}</span>"

        html.append(f"<a href=\"{link}\" class=\"list-group-item list-group-item-action\">")
        html.append("<div class=\"row\">")
        #html.append(f"<div class=\"col-s-2 col-xs-12 p-1 publication-year-box\">{year}</div>")
        html.append(f"<div class=\"col-s-10 col-xs-12 p-1 publication-cite-box\">{year}<br/><br/>{title}<br/><br/>{journal} {meta}<br/><br/>{authors}</div>")
        html.append("</div>")
        html.append("</a>")

    html.append("</div>")
    return "".join(html)

def to_funding(df):
    """
    Create pretty funding list.
    """

    # Break projects into rows
    out = [[]]

    col_counter = 0
    for i in range(len(df)):

        row = df.iloc[i,:]
        width = row["width"]

        col_counter += width
        if col_counter > 12:
            out.append([])
            col_counter = 0

        lg = 2*width
        sm = 2*width
        col_div = f"<div class=\"col-lg-{lg} col-sm-{sm} col-xs-12\">"

        out[-1].append({"title":row["title"],
                        "img":"img/funding/{}".format(row["img"]),
                        "link":row["link"],
                        "col_div":col_div})
    html = []
    for row in out:
        html.append("<div class=\"row mx-auto\">")
        for i in range(len(row)):
            img = row[i]["img"]
            title = row[i]["title"]
            link = row[i]["link"]

            html.append(row[i]["col_div"])
            html.append(generate_hover(img,title,link=link,text_class="white-text fund-text",image_class="img-fluid"))
            html.append("</div>")

        html.append("</div>")
        html.append("<br/>")

    return "".join(html)

def parse_markdown(md_file):
    """
    Create pretty html from a markdown file.
    """

    f = open(md_file)
    md = f.read()
    f.close()

    md_parser = mistune.Markdown()

    html = md_parser(md)

    img_pattern = re.compile("<img ")
    html = img_pattern.sub("<img class=\"img-fluid\"",html)

    html = re.sub("<ul>","<ul class=\"list-group\">",html)
    html = re.sub("<li>","<li class=\"list-group-item\">",html)

    h1_pattern = re.compile("<h1>.*?</h1>")
    h1_matches = h1_pattern.findall(html)
    if h1_matches:
        for m in h1_matches:
            inner = m.split(">")[1].split("<")[0]
            inner = inner.lower()
            inner = re.sub(" ","-",inner)

            new_header = f"<h1 id=\"{inner}\">{m[4:]}"

            html = re.sub(m,new_header,html)

    hr_pattern = re.compile("\<hr\>")

    out = []
    out.append("<br/><br/>")
    for section in hr_pattern.split(html):
        out.append("<div class=\"container bg-light rounded mx-auto\">")
        out.append("<div class=\"m-3 p-3\">")
        out.append(section)
        out.append("</div></div><br/>")


    return "".join(out)


def generate_index(page_file,template_file):
    """
    Generate an index file.  Do so given a pages.xlsx file and a template
    html file.
    """

    session = {}

    # Projects
    df = pd.read_excel(page_file,sheet_name="projects")
    session["projects"] = to_projects(df)

    # People
    df = pd.read_excel(page_file,sheet_name="people")
    session["current_people"] = to_people(df[df.status == "current"])
    session["previous_people"] = to_people(df[df.status == "previous"])

    # Publications
    df = pd.read_excel(page_file,sheet_name="publications")
    session["publications"] = to_publications(df)

    # Funding
    df = pd.read_excel(page_file,sheet_name="funding")
    session["current_funding"] = to_funding(df[df.status == "current"])
    session["previous_funding"] = to_funding(df[df.status == "previous"])

    # Use junja to make html
    session_to_html(session,template_file,"index.html")

def generate_from_markdown(md_file,template_file):
    """
    Use jinja to load content from markdown into a template file.
    """

    session = {}
    session["content"] = parse_markdown(md_file)

    root = ".".join(md_file.split(".")[:-1])
    session_to_html(session,template_file,f"{root}.html")


def session_to_html(session,template_file,output_file):
    """
    Use jinja load generated html into an html file.
    """

    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader,
                                      autoescape=jinja2.select_autoescape("html"))
    template = template_env.get_template(template_file)
    output = template.render(session=session)

    f = open(output_file,"w")
    f.write(output)
    f.close()

def install_into(target_dir):

    if os.path.isdir(target_dir):
        shutil.rmtree(target_dir)

    os.mkdir(target_dir)

    html_files = glob.glob("*.html",recursive=True)
    to_whack = re.compile("_template.html")
    html_files = [f for f in html_files if not to_whack.search(f)]

    if os.path.isfile("CNAME"):
        html_files.append("CNAME")

    dirs = [d for d in os.listdir() if os.path.isdir(d) and d[0] != "."]

    for f in html_files:
        shutil.copy(f,target_dir)


    for d in dirs:
        shutil.copytree(d,os.path.join(target_dir,d))


def main(argv=None):

    if argv is None:
        argv = sys.argv[1:]

    try:
        source_dir = argv[0]
    except IndexError:
        err = f"Incorrect arguments. Usage:\n\n{__usage__}\n\n"
        raise ValueError(err)

    # Figure out if we are installing into target_dir
    try:
        target_dir = argv[1]
        target_dir = os.path.abspath(target_dir)
    except IndexError:
        target_dir = None

    os.chdir(source_dir)
    page_file = "pages.xlsx"
    index_template = "index_template.html"
    basic_template = "basic_template.html"

    generate_index(page_file,index_template)

    # Generate markdown files
    for md_file in glob.glob("*.md"):
        generate_from_markdown(md_file,basic_template)

    if target_dir is not None:
        install_into(target_dir)




if __name__ == "__main__":
    main()

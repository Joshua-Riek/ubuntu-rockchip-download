import json
import datetime
import os
import subprocess
import tempfile

top = """<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <title>Ubuntu Rockchip</title>
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.4/dist/jquery.min.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"
            crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/moment@2.29.4/moment.min.js" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
          crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.min.css"
          crossorigin="anonymous">
    <style>
        body {{
            padding-top: 4.5rem;
        }}

        .pill {{
            border-radius: 50px;
        }}

        code.shell-root:before {{
            content: "# ";
        }}

        code.shell-normal:before {{
            content: "$ ";
        }}

        pre.wrap {{
            white-space: pre-wrap;
        }}
    </style>
</head>
<body data-new-gr-c-s-check-loaded="14.1043.0" data-gr-ext-installed="">
<header>
    <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse"
                    aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <a class="navbar-brand" href="../">Ubuntu Rockchip</a>
            <div class="collapse navbar-collapse" id="navbarCollapse">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link" href="../">Supported boards</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="https://github.com/Joshua-Riek/ubuntu-rockchip">Source code</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="https://github.com/Joshua-Riek/ubuntu-rockchip/issues">Issues</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="https://github.com/Joshua-Riek/ubuntu-rockchip/discussions">Discussions</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="https://github.com/Joshua-Riek/ubuntu-rockchip/wiki">Wiki</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</header>
<main>
    <div class="container">
        <h2>Downloads for the {0}</h2>
        <p>Ubuntu Linux images for various ARM-based single board computers (SBCs).</p>
        <hr>
    </div>
    <div class="container">
        <table class="table table-sm table-hover">
            <thead>
            <tr>
                <th scope="col">File</th>
                <th scope="col">Last modified</th>
                <th scope="col">Size</th>
                <th scope="col">Description</th>
            </tr>
            </thead>
            <tbody>
"""

item = """
            <tr>
                <td>
                    <a href="{0}">{1}</a>
                </td>
                <td>{2}</td>
                <td>{3}</td>
                <td>{4}</td>
            </tr>"""

bottom = """
            </tbody>
        </table>
        <hr>
    </div>
</main>
</body>
</html>
"""


def humanbytes(B):
    """Return the given bytes as a human friendly KB, MB, GB, or TB string."""
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

    if B < KB:
        return '{0}'.format(int(B))
    elif KB <= B < MB:
        return '{0:.1f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.1f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.1f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.1f} TB'.format(B / TB)


def get_var(varname, script):
    CMD = 'echo $(source ' + script + '; echo $%s)' % varname
    p = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
    return p.stdout.readlines()[0].strip()


with tempfile.TemporaryDirectory() as tmpdir:
    os.system("git clone https://github.com/Joshua-Riek/ubuntu-rockchip.git " + tmpdir)
    with tempfile.NamedTemporaryFile() as tmpfile:
        os.system("curl https://api.github.com/repos/Joshua-Riek/ubuntu-rockchip/releases -o " + str(tmpfile.name))
        data = json.loads(tmpfile.read())

    boards = []
    for y in data[0]["assets"]:
        if y["name"].endswith(".sha256"):
            desc = "-"
        elif "desktop" in y["name"]:
            if "24.04" in y["name"]:
                desc = "Ubuntu 24.04 LTS Desktop with Linux 6.1"
            else:
                desc = "Ubuntu 22.04 LTS Desktop with Linux 5.10"
        elif "server" in y["name"]:
            if "24.04" in y["name"]:
                desc = "Ubuntu 24.04 LTS Server with Linux 6.1"
            else:
                desc = "Ubuntu 22.04 LTS Server with Linux 5.10"
        else:
            desc = "-"

        boards.append([y["browser_download_url"], y["name"],
                       datetime.datetime.strptime(y["updated_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M"),
                       humanbytes(y["size"]), desc])

    for y in os.listdir(tmpdir + "/config/boards/"):
        file = open("%s" % "boards/" + y[:-2] + "html", "w")
        file.write(top.format(get_var('BOARD_NAME', tmpdir + "/config/boards/" + y).decode()))
        for x in boards:
            if y[:-2] in x[1]:
                file.write(item.format(x[0], x[1], x[2], x[3], x[4]))
        file.write(bottom)
        file.close()

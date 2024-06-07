import json
import datetime
import os

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
        <h2>Downloads for {0}</h2>
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

os.system("curl https://api.github.com/repos/Joshua-Riek/ubuntu-rockchip/releases -o ubuntu-orange-pi5.json")

def format_bytes(size):
    # 2**10 = 1024
    power = 2 ** 10
    n = 0
    power_labels = {0: '', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    if n == 0:
        return str(size)
    return str(format(size, '0.1f')) + " " + power_labels[n]

def humanbytes(B):
    """Return the given bytes as a human friendly KB, MB, GB, or TB string."""
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2) # 1,048,576
    GB = float(KB ** 3) # 1,073,741,824
    TB = float(KB ** 4) # 1,099,511,627,776

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

file1 = open("ubuntu-orange-pi5.json", "r")
data = json.loads(file1.read())
file1.close()

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
            desc = "Ubuntu 24.04 LTS Desktop with Linux 6.1"
        else:
            desc="Ubuntu 22.04 LTS Server with Linux 5.10"
    else:
        desc = "-"

    boards.append([y["browser_download_url"], y["name"],
                   datetime.datetime.strptime(y["updated_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M"),
                   humanbytes(y["size"]), desc])

def create_html(filename, query_name, pretty_name):
    file = open("%s" % filename, "w")
    file.write(top.format(pretty_name))
    for x in boards:
        if query_name in x[1]:
            file.write(item.format(x[0], x[1], x[2], x[3], x[4]))
    file.write(bottom)
    file.close()


create_html("boards/orangepi-5.html", "orangepi-5.", "Orange Pi 5")
create_html("boards/orangepi-5b.html", "orangepi-5b.", "Orange Pi 5B")
create_html("boards/orangepi-5-plus.html", "orangepi-5-plus.", "Orange Pi 5 Plus")
create_html("boards/orangepi-5-pro.html", "orangepi-5-pro.", "Orange Pi 5 Pro")
create_html("boards/rock-5a.html", "rock-5a.", "ROCK 5A")
create_html("boards/rock-5b.html", "rock-5b.", "ROCK 5B")
create_html("boards/rock-5c.html", "rock-5c.", "ROCK 5C")
create_html("boards/rock-5d.html", "rock-5d.", "ROCK 5D")
create_html("boards/rock-5b-plus.html", "rock-5b-plus.", "ROCK 5B Plus")
create_html("boards/radxa-cm5-io.html", "radxa-cm5-io.", "Radxa CM5 IO")
create_html("boards/nanopi-r6c.html", "nanopi-r6c.", "NanoPi R6C")
create_html("boards/nanopi-r6s.html", "nanopi-r6s.", "NanoPi R6S")
create_html("boards/nanopc-t6.html", "nanopc-t6.", "NanoPC T6")
create_html("boards/mixtile-blade3.html", "mixtile-blade3.", "Mixtile Blade 3")
create_html("boards/lubancat-4.html", "lubancat-4.", "LubanCat 4")
create_html("boards/indiedroid-nova.html", "indiedroid-nova.", "Indiedroid Nova")
create_html("boards/turing-rk1.html", "turing-rk1.", "Turing RK1")
create_html("boards/roc-rk3588s-pc.html", "roc-rk3588s-pc.", "ROC RK3588S PC")
create_html("boards/armsom-w3.html", "armsom-w3.", "ArmSoM w3")
create_html("boards/armsom-sige7.html", "armsom-sige7.", "ArmSoM Sige7")
create_html("boards/radxa-nx5-io.html", "radxa-nx5-io.", "Radxa NX5 IO")
create_html("boards/rock-5-itx.html", "rock-5-itx.", "ROCK 5 ITX")
create_html("boards/mixtile-core3588e.html", "mixtile-core3588e.", "Mixtile Core 3588E")
create_html("boards/radxa-zero3.html", "radxa-zero3.", "Radxa Zero 3")
create_html("boards/orangepi-3b.html", "orangepi-3b.", "Orange Pi 3B")

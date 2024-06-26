import os
import subprocess
import tempfile
from collections import OrderedDict

top = """<html lang="en" ma1="ma"><head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <title>Ubuntu Rockchip</title>
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.4/dist/jquery.min.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/moment@2.29.4/moment.min.js" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.min.css" crossorigin="anonymous">
    <style>
        body  {
            padding-top: 4.5rem;
        }
        .pill {
            border-radius: 50px;
        }
        code.shell-root:before {
            content: "# ";
        }
        code.shell-normal:before {
            content: "$ ";
        }
        pre.wrap {
            white-space: pre-wrap;
        }
    </style>
    <meta http-equiv="origin-trial" content="AymqwRC7u88Y4JPvfIF2F37QKylC04248hLCdJAsh8xgOfe/dVJPV3XS3wLFca1ZMVOtnBfVjaCMTVudWM//5g4AAAB7eyJvcmlnaW4iOiJodHRwczovL3d3dy5nb29nbGV0YWdtYW5hZ2VyLmNvbTo0NDMiLCJmZWF0dXJlIjoiUHJpdmFjeVNhbmRib3hBZHNBUElzIiwiZXhwaXJ5IjoxNjk1MTY3OTk5LCJpc1RoaXJkUGFydHkiOnRydWV9"></head>
<body data-new-gr-c-s-check-loaded="14.1043.0" data-gr-ext-installed="">
<header>
    <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <a class="navbar-brand" href="./">Ubuntu Rockchip</a>
            <div class="collapse navbar-collapse" id="navbarCollapse">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link" href="./">Supported boards</a>
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
        <h2>Supported boards</h2>
        <p>Ubuntu Linux images for various ARM-based single board computers (SBCs).</p>
        <hr>
    </div>
    <div class="container">
        <table class="table table-sm table-hover">
            <thead>
            <tr>
                <th scope="col">Board</th>
                <th scope="col">Vendor</th>
                <th scope="col">SOC</th>
                <th scope="col">CPU</th>
            </tr>
            </thead>
            <tbody>

"""

item = """
            <tr data-href="{0}">
                <td><a href="{0}">{1}</a></td>
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


def get_var(varname, script):
    CMD = 'echo $(source ' + script + '; echo $%s)' % varname
    p = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
    return p.stdout.readlines()[0].strip().decode()


def get_boards():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.system("git clone https://github.com/Joshua-Riek/ubuntu-rockchip.git " + tmpdir)

        boards = OrderedDict()
        for board in sorted(os.listdir(tmpdir + "/config/boards/")):
            boards[board[:-3]] = {
                "BOARD_NAME": get_var('BOARD_NAME', tmpdir + "/config/boards/" + board),
                "BOARD_MAKER": get_var('BOARD_MAKER', tmpdir + "/config/boards/" + board),
                "BOARD_SOC": get_var('BOARD_SOC', tmpdir + "/config/boards/" + board),
                "BOARD_CPU": get_var('BOARD_CPU', tmpdir + "/config/boards/" + board),
            }
        return boards


def format_html(boards):
    text = []
    for board in boards:
        text.append(item.format(
            "./boards/" + board + ".html",
            boards[board]["BOARD_NAME"],
            boards[board]["BOARD_MAKER"],
            boards[board]["BOARD_SOC"],
            boards[board]["BOARD_CPU"],
        ))
    return top + ''.join(text) + bottom


if __name__ == "__main__":
    boards = get_boards()

    tmp = boards["roc-rk3588s-pc"]
    del boards["roc-rk3588s-pc"]
    boards["roc-rk3588s-pc"] = tmp
    boards.move_to_end("turing-rk1")

    index_html = format_html(boards)
    with open("index.html", "w") as file:
        file.write(index_html)

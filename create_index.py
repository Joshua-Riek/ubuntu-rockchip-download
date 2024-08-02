import os
import subprocess
import tempfile
from collections import OrderedDict

top = """<html lang="en" data-bs-theme="auto">
<head>
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
        body {
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
        table {
            line-height: 1.5;
            padding: .25rem .25rem;
        }
    </style>
    <script>
        if ($("html").attr("data-bs-theme") === "auto") {
            const prefersColorSchemeQuery = "(prefers-color-scheme: dark)";
            function updateTheme() {
                const prefersDark = window.matchMedia(prefersColorSchemeQuery).matches;
                $("html").attr("data-bs-theme", prefersDark ? "dark" : "light");
            }
            window.matchMedia(prefersColorSchemeQuery).addEventListener("change", updateTheme);
            updateTheme();
        }
    </script>
</head>
<header>
    <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-black">
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
        <p>Ubuntu 22.04 and 24.04 for various Rockchip single board computers (SBCs).</p>
        <hr>
    </div>
    <div class="container">
        <table class="table table-sm table-hover" >
            <caption>Supported boards.</caption>
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

BOARD_TEMPLATE = """
            <tr>
                <td><a href="{0}">{BOARD_NAME}</a></td>
                <td>{BOARD_MAKER}</td>
                <td>{BOARD_SOC}</td>
                <td>{BOARD_CPU}</td>
            </tr>"""

bottom = """
            </tbody>
        </table>
        <hr>
    </div>
</main>
<footer class="container">
    <p class="float-end"><a href="#">Back to top</a></p>
    <p>This project is not officially affiliated with Canonical Ltd or Fuzhou Rockchip Electronics Co., Ltd.</p>
</footer>
</html>
"""


def get_var(varname, script):
    CMD = 'echo $(source ' + script + '; echo $%s)' % varname
    p = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
    return p.stdout.readlines()[0].strip().decode()


def get_boards():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.system("git clone https://github.com/Joshua-Riek/ubuntu-rockchip.git " + tmpdir)

        boards = []
        for board in sorted(os.listdir(tmpdir + "/config/boards/")):
            boards.append( {
                "BOARD_NAME": get_var('BOARD_NAME', tmpdir + "/config/boards/" + board),
                "BOARD_MAKER": get_var('BOARD_MAKER', tmpdir + "/config/boards/" + board),
                "BOARD_SOC": get_var('BOARD_SOC', tmpdir + "/config/boards/" + board),
                "BOARD_CPU": get_var('BOARD_CPU', tmpdir + "/config/boards/" + board),
                "id": board[:-3],
            })
        boards.sort(key=lambda row: row["BOARD_NAME"])

        return boards


def format_html(boards):
    text = []
    for i, v in enumerate(boards):
        text.append(BOARD_TEMPLATE.format("./boards/" + v['id'] + ".html", **v))
    return top + ''.join(text) + bottom


if __name__ == "__main__":
    boards = get_boards()

    index_html = format_html(boards)
    with open("index.html", "w") as file:
        file.write(index_html)

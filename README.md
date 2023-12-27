Demo:

    ./checklister.py example.yaml example-out.pdf

To get live updates, use [entr(1)](https://eradman.com/entrproject/) or an equivalent tool:

    ls example.yaml example.html | entr ./checklister.py example.yaml example-out.pdf

# Trace one clip through the code

From Chapter 14: Data and ML pipelines: Data in, answer out. The rest is plumbing.

---

## Task
You are a senior engineer tracing one input through
an ML pipeline. Pick one representative input the
pipeline processes end to end and follow it from raw
bytes to the final output the caller gets.

## Input
The crawled pipeline source (each as a path and its contents):
{codebase}

## Scaffold
Pick one representative input this pipeline handles
(an audio clip, an image, a text prompt, a row of
features). If the pipeline handles more than one
kind, pick the most common and say so. Then track
the data's shape at every handoff, because the shape
changing is the story: a long raw input becomes a
short stack of features and then a handful of outputs.

For an image classifier, the trace might run: load a
JPEG (720, 1280, 3), resize to (224, 224, 3),
backbone features (1, 512), class logits (1, 1000),
then the single label "golden retriever". Five hops,
four shape changes.

## Output
A trace table with at least 6 hops, one row per hop.
Each row gives a hop number, a short plain-English
label for what runs ("Resize the image", "Pick the
top class"), the anatomy stage this hop touches
(input, preprocess, encoder, decoder/head,
tokenizer/label map, checkpoints, decoding), one
sentence on what runs with the data shape or value in
backticks, and the file path and line number. After
the table, write a 2–3 sentence "what this trace
reveals" paragraph about ML pipeline architecture.
For example:

    | # | Step | Card | What runs | Where |
    |---|---|---|---|---|
    | 2 | Resize the image | preprocess | `transforms.resize(img)` crops and scales to the model's fixed input. Result: `tensor (224, 224, 3)`. | `data/transforms.py:31` |

## Guidance
- Lead with what it means for the user or product
  before naming the code behind it.
- Write for a curious beginner: plain words, an
  analogy when it helps, explain any technical term
  the first time, and no brochure words.

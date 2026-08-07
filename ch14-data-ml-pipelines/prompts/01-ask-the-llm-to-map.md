# Ask the LLM to map the six stages

From Chapter 14: Data and ML pipelines: Data in, answer out. The rest is plumbing.

---

## Task
You are a senior engineer reading an ML pipeline's
source for the first time. Draw a one-page map of the
stages one input passes through, in order, from raw
bytes to the final output.

## Input
The crawled pipeline source (each as a path and its contents):
{codebase}

## Scaffold
Most inference pipelines move through some version of
the stages below, but every repo names them
differently and some skip a few. Treat the list as a
checklist, not a required set: cover whatever this
pipeline has, note what it lacks, and decide which
stages earn a row. Show the trained weights as a
checkpoint loaded off to the side, not as a stage in
the flow.
  1. Input loading (an audio file, an image, a text
     prompt, a row of features).
  2. Preprocessing (raw input → model-ready tensor:
     a spectrogram for sound, resized patches for an
     image, token ids for text).
  3. Encoder (summarize the input into a compact
     internal representation).
  4. Decoder or head (produce the output: a text
     decoder, a classifier head, a regression head).
  5. Tokenizer or label map (how the output maps back
     to something readable).
  6. Decoding strategy (the output loop: greedy, beam
     search, sampling, argmax).

For an image classifier, the map might run: load a
JPEG, resize it to a fixed (224, 224, 3) tensor, run
a convolutional backbone (the neural net), pass a
classifier head, then a label map from class id to
name. There is no decoding loop, so you would note
that this pipeline skips it.

## Output
A stage map with one row per stage this pipeline has.
Each row gives the data shape going in and the shape
coming out, one tag marking the stage as THE NEURAL
NET or GLUE around it, and one sentence naming the
single choice this team made here that another team
might have made differently (which input library,
which preprocessing transform, which decoding
strategy on a bad guess). For example:

    | # | Stage | In → Out | Net or glue | What the team picked |
    |---|---|---|---|---|
    | 2 | Resize | `(720,1280,3) → (224,224,3)` | GLUE | Center-crop instead of squashing, so wide photos keep their shape. |

## Guidance
- Lead with what it means for the user or product
  before naming the code behind it.
- Write for a curious beginner: plain words, an
  analogy when it helps, explain any technical term
  the first time, and no brochure words.

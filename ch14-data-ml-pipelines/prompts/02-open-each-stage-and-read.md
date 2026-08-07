# Open each stage and read the code inside it

From Chapter 14: Data and ML pipelines: Data in, answer out. The rest is plumbing.

---

## Task
You are a senior engineer reading an ML pipeline's
source for the first time. Fill in a pipeline
anatomy, one card per stage.

## Input
The crawled pipeline source (each as a path and its contents):
{codebase}

## Scaffold
Most inference pipelines are built from some version
of the stages below: three that follow the input,
transform, output shape (input loading, encoder,
decoder/output) plus a few practical add-ons
(preprocessing, a vocabulary or label map,
checkpoints, a decoding strategy). Treat the list as
a checklist, not a required set: cover the stages
this pipeline has, flag the ones it doesn't, and
decide which deserve a card.

  1. Input loading (what the system accepts, what it
     rejects)
  2. Preprocessing (the shape transform that turns
     raw input into a model-ready tensor)
  3. Encoder (the function that summarizes the input
     into a compact internal representation)
  4. Decoder or head (the function that produces the
     output from that summary plus previous outputs)
  5. Tokenizer or label map (the vocabulary contract:
     how bytes become ids and back)
  6. Checkpoints (where the trained weights live on
     disk and how they get loaded)
  7. Decoding strategy (the reliability layer: beam
     search, fallback, thresholds)

For an image classifier, the preprocessing card might
read: the resize step turns a (720, 1280, 3) photo
into the fixed (224, 224, 3) tensor the model expects,
and the mean/std normalization constants at L14 are
baked into the trained weights, so changing them
silently breaks accuracy.

## Output
One bold-headline paragraph per stage the pipeline
has, in slot order. The headline names the slot, the
file path, and the most distinctive fact (LOC,
dependency, or constant). The body (4–6 sentences)
names what input or output transformation this slot
performs for the user, the shape going in and the
shape coming out, the hardcoded constants the
trained weights depend on, and the file:line pointers
that prove it. For example:

    **Card 2 (preprocessing): `transforms.py` is 60 LOC and resizes every image to 224×224.**
    The loader hands over a full-size photo, but the model only reads a fixed square, so this stage shrinks it. A `(720, 1280, 3)` array becomes `(224, 224, 3)`, then gets normalized by the mean/std constants at L14 that the weights were trained against.

## Guidance
- Open each card after the first with a one-sentence
  transition naming the new stage of the pipeline
  this slot adds that the previous didn't; don't
  recap.
- Lead with what it means for the user or product
  before naming the code behind it.
- Write for a curious beginner: plain words, an
  analogy when it helps, explain any technical term
  the first time, and no brochure words.

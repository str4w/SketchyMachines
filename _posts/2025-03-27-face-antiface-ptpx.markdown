---
layout: post
title:  "Face and Antiface, a postcard for PTPX24"
date:   2025-03-27 12:28:33 +0000
categories: Art; Machine Learning
---
PTPX is a roughly yearly plotter postcard exchange which is always a lot of fun to participate in. I’ve been wanting to. mix neural and classical algorithmic approaches for a while and took this as an opportunity to start doing that. I had also resolved to start releasing more of the code for these projects, so here it is. Here is my postcard for this year, entitled Face and Antiface.

![A plotted postcard in black and blue ink on white paper, of two faces rendered using halftoning with a bar code between them.](/assets/2025-03-27-face-antiface-ptpx/face_antiface.jpg)

These faces are not of real people, any resemblance. is purely coincidental. They are generated from the 128 dimensional latent space of a small convolutional variational autoencoder. trained on a dataset of human faces. Each pair is from a random binary vector scaled to the approximate limits. of reasonable faces. One face is rendered from the negative of the vector for the other, placing them at opposite corners. of a 128 dimensional box of faces. The bar code between them is the vector itself.

Plotter enthusiasts will want to know that these were done with Staedler Triplus markers on cardstock using my antique Roland DXY-885.

This post goes into more detail on the method, and links to the code and models.

Concept
=======

An autoencoder is an encoder / decoder pair where an encoder maps samples from some population into a latent space,. and the decoder maps the latent space back to the original population. A variational autoencoder maps samples to a latent space constrained to be a probability distribution (usually Gaussian). It is easy to generate. samples from a variational autoencoder.

Unlike GANs, the losses used when training a VAE are a simple reconstruction loss and the probability distribution. constraint, no discriminator. VAE’s tend to give blurrier results; for this artistic purpose, that was fine.

After generation of the image pair, however, these had to be converted to something renderable on the plotter. I.
chose to use a halftone for this, and to render the latent vector as a barcode in the middle.

Preparing the dataset 
=====================

The dataset of faces used was https://www.kaggle.com/datasets/yapwh1208/face-data Aesthetically, I felt this looked better if. the background was a separate color. Of course, this meant that the background had to be identified. To do so, the segmentation. models toolkit was used along with 99 hand segmented faces selected at random from the dataset. It only required hand-segmenting a few to have enough examples to train a little model to do the rest. Once a segmentation model was created, masks for the entire. dataset were generated.

If you want to play along, you don’t have to do this, as the segmentation masks are now available on Kaggle.

- [Notebook](https://github.com/str4w/FaceAndAntiface/blob/main/MaskFaces.ipynb)
- [Model](https://huggingface.co/TiredRobot/SimpleFaceSegmentation)
- [Face Dataset](https://www.kaggle.com/datasets/yapwh1208/face-data)
- [Hand drawn masks for bootstrapping](https://www.kaggle.com/datasets/tiredrobot/hand-drawn-face-masks-for-yapwh-face-data )
- [Mask Dataset](https://www.kaggle.com/datasets/tiredrobot/model-generated-face-masks-for-yapwh-face-data)

Training the autoencoder
========================

The autoencoder is a very simple convolutional autoencoder which reconstructs the masked versions of the faces. In addition to. the reconstruction loss, additional losses on the gender classification and age regression are used. It is debatable how much impact they. actually have though - they are there more because I stopped frigging with it at that point, not because I actually found an aesthetic. impact on the output.

Interestingly, in an early iteration of this project when all faces were used, I found that one of the face pairs nearly always looked. like a child. This old-young distinction wasn’t what I was going for, so I limited the training dataset to people older than 15.

The autoencoder output is quite blurry, and does not capture many kinds of details at all. I have not seen it generate glasses or beards. for example. As an artistic rendering of a face this is fine, maybe even interesting.

- [Notebook](https://github.com/str4w/FaceAndAntiface/blob/main/Autoencode_Faces.ipynb)
- [Model](https://huggingface.co/TiredRobot/FaceVAE)

Generating faces
================

There are a range of vectors around zero in the latent space that generate plausible faces. Vectors too far from zero generate a mess… I estimated “how far” in an entirely adhoc way, by looking at the range of the latent vector in a handful of reconstructions.

Then to generate the faces for the postcards, a random binary vector was generated, mapped to -1 and 1 instead of 0 and 1, and scaled to this estimated range. Is this hokey in a lot of ways? Of course it is - but it’s postcard.

Preparing the plottable
=======================

To make the plottable version of this, I used a halftoning process. The intensity at a grid of points across the image is accumulated by averaging a block of pixels around each point. Absolutely no signal processing knowledge was applied, but in the end there is no visible ringing or other signal distortion so I just carried on with my first hack. The halftone was intended to be on a staggered. grid, but in doing the math wrong, it ended up aligned on one edge and staggered on the other. I liked it, so I kept it in.

The halftone circles are filled by drawing a spiral - originally multiple circles were used, but the lifting and lowering of the pen was slow, noisy and left weird ink blobs at the start and stop positions.

You’ll find the code for this in the autoencoder notebook as well.

Conclusion
==========

And that’s a wrap. As usual, it took far far longer to get these PTPX postcards out than I ever intended. However, it seems I’m. not the only one that happens to. At least I haven’t taken so long yet that the next PTPX started already!

"""
Generate "Attention Is All You Need" Paper
==========================================

Recreates the famous Transformer paper using WAFT's academic paper template.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.templates.academic_paper import generate_academic_paper


def main():
    """Generate the Attention Is All You Need paper."""

    # Paper metadata
    title = "Attention Is All You Need"

    authors = [
        {"name": "Ashish Vaswani"},
        {"name": "Noam Shazeer"},
        {"name": "Niki Parmar"},
        {"name": "Jakob Uszkoreit"},
        {"name": "Llion Jones"},
        {"name": "Aidan N. Gomez"},
        {"name": "Łukasz Kaiser"},
        {"name": "Illia Polosukhin"},
    ]

    affiliations = ["Google Brain", "Google Research", "University of Toronto"]

    abstract = """
    The dominant sequence transduction models are based on complex recurrent or 
    convolutional neural networks that include an encoder and a decoder. The best 
    performing models also connect the encoder and decoder through an attention mechanism. 
    We propose a new simple network architecture, the Transformer, based solely on 
    attention mechanisms, dispensing with recurrence and convolutions entirely. 
    Experiments on two machine translation tasks show that these models are superior 
    in quality while being more parallelizable and requiring significantly less time 
    to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation 
    task, improving over the existing best results, including ensembles, by over 2 BLEU. 
    On the WMT 2014 English-to-French translation task, our model establishes a new 
    single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on 
    eight GPUs, a small fraction of the training costs of the best models from the 
    literature. We show that the Transformer generalizes well to other tasks by applying 
    it successfully to English constituency parsing with large and limited training data.
    """

    # Main content
    content = """
    <h1>Introduction</h1>
    
    <p>Recurrent neural networks, long short-term memory and gated recurrent neural 
    networks in particular, have been firmly established as state of the art approaches 
    in sequence modeling and transduction problems such as language modeling and machine 
    translation. Numerous efforts have since continued to push the boundaries of 
    recurrent language models and encoder-decoder architectures.</p>
    
    <p>Recurrent models typically factor computation along the symbol positions of the 
    input and output sequences. Aligning positions to steps in computation time, they 
    generate a sequence of hidden states h<sub>t</sub>, as a function of the previous 
    hidden state h<sub>t-1</sub> and the input for position t. This inherently sequential 
    nature precludes parallelization within training examples, which becomes critical at 
    longer sequence lengths, as memory constraints limit batching across examples. Recent 
    work has achieved significant improvements in computational efficiency through 
    factorization tricks and conditional computation, while also improving model 
    performance in case of the latter. The fundamental constraint of sequential 
    computation, however, remains.</p>
    
    <p>Attention mechanisms have become an integral part of compelling sequence modeling 
    and transduction models in various tasks, allowing modeling of dependencies without 
    regard to their distance in the input or output sequences. In all but a few cases, 
    however, such attention mechanisms are used in conjunction with a recurrent network.</p>
    
    <p>In this work we propose the Transformer, a model architecture eschewing recurrence 
    and relying entirely on an attention mechanism to draw global dependencies between 
    input and output. The Transformer allows for significantly more parallelization and 
    can reach a new state of the art in translation quality after being trained for as 
    little as twelve hours on eight P100 GPUs.</p>
    
    <h1>Background</h1>
    
    <p>The goal of reducing sequential computation also forms the foundation of the 
    Extended Neural GPU, ByteNet and ConvS2S, all of which use convolutional neural 
    networks as basic building block, computing hidden representations in parallel for 
    all input and output positions. In these models, the number of operations required 
    to relate signals from two arbitrary input or output positions grows in the distance 
    between positions, linearly for ConvS2S and logarithmically for ByteNet. This makes 
    it more difficult to learn dependencies between distant positions. In the Transformer 
    this is reduced to a constant number of operations, albeit at the cost of reduced 
    effective resolution due to averaging attention-weighted positions, an effect we 
    counteract with Multi-Head Attention.</p>
    
    <p>Self-attention, sometimes called intra-attention, is an attention mechanism 
    relating different positions of a single sequence in order to compute a representation 
    of the sequence. Self-attention has been used successfully in a variety of tasks 
    including reading comprehension, abstractive summarization, textual entailment and 
    learning task-independent sentence representations. End-to-end memory networks are 
    based on a recurrent attention mechanism instead of sequence-aligned recurrence and 
    have been shown to perform well on simple-language question answering and language 
    modeling tasks.</p>
    
    <p>To the best of our knowledge, however, the Transformer is the first transduction 
    model relying entirely on self-attention to compute representations of its input and 
    output without using sequence-aligned RNNs or convolution.</p>
    
    <h1>Model Architecture</h1>
    
    <p>Most competitive neural sequence transduction models have an encoder-decoder 
    structure. Here, the encoder maps an input sequence of symbol representations 
    (x<sub>1</sub>, ..., x<sub>n</sub>) to a sequence of continuous representations 
    z = (z<sub>1</sub>, ..., z<sub>n</sub>). Given z, the decoder then generates an 
    output sequence (y<sub>1</sub>, ..., y<sub>m</sub>) of symbols one element at a 
    time. At each step the model is auto-regressive, consuming the previously generated 
    symbols as additional input when generating the next.</p>
    
    <p>The Transformer follows this overall architecture using stacked self-attention 
    and point-wise, fully connected layers for both the encoder and decoder, shown in 
    the left and right halves of Figure 1, respectively.</p>
    
    <h2>3.1 Encoder and Decoder Stacks</h2>
    
    <h3>Encoder:</h3>
    <p>The encoder is composed of a stack of N = 6 identical layers. Each layer has 
    two sub-layers. The first is a multi-head self-attention mechanism, and the second 
    is a simple, position-wise fully connected feed-forward network. We employ a residual 
    connection around each of the two sub-layers, followed by layer normalization. That 
    is, the output of each sub-layer is LayerNorm(x + Sublayer(x)), where Sublayer(x) is 
    the function implemented by the sub-layer itself. To facilitate these residual 
    connections, all sub-layers in the model, as well as the embedding layers, produce 
    outputs of dimension d<sub>model</sub> = 512.</p>
    
    <h3>Decoder:</h3>
    <p>The decoder is also composed of a stack of N = 6 identical layers. In addition 
    to the two sub-layers in each encoder layer, the decoder inserts a third sub-layer, 
    which performs multi-head attention over the output of the encoder stack. Similar to 
    the encoder, we employ residual connections around each of the sub-layers, followed 
    by layer normalization. We also modify the self-attention sub-layer in the decoder 
    stack to prevent positions from attending to subsequent positions. This masking, 
    combined with the fact that the output embeddings are offset by one position, ensures 
    that the predictions for position i can depend only on the known outputs at positions 
    less than i.</p>
    
    <h2>3.2 Attention</h2>
    
    <p>An attention function can be described as mapping a query and a set of key-value 
    pairs to an output, where the query, keys, values, and output are all vectors. The 
    output is computed as a weighted sum of the values, where the weight assigned to each 
    value is computed by a compatibility function of the query with the corresponding key.</p>
    
    <h3>3.2.1 Scaled Dot-Product Attention</h3>
    
    <p>We call our particular attention "Scaled Dot-Product Attention" (Figure 2). The 
    input consists of queries and keys of dimension d<sub>k</sub>, and values of dimension 
    d<sub>v</sub>. We compute the dot products of the query with all keys, divide each by 
    √d<sub>k</sub>, and apply a softmax function to obtain the weights on the values.</p>
    
    <p>In practice, we compute the attention function on a set of queries simultaneously, 
    packed together into a matrix Q. The keys and values are also packed together into 
    matrices K and V. We compute the matrix of outputs as:</p>
    
    <div class="equation">
        Attention(Q, K, V) = softmax(QK<sup>T</sup> / √d<sub>k</sub>)V
    </div>
    
    <h3>3.2.2 Multi-Head Attention</h3>
    
    <p>Instead of performing a single attention function with d<sub>model</sub>-dimensional 
    keys, values and queries, we found it beneficial to linearly project the queries, keys 
    and values h times with different, learned linear projections to d<sub>k</sub>, 
    d<sub>k</sub> and d<sub>v</sub> dimensions, respectively. On each of these projected 
    versions of queries, keys and values we then perform the attention function in parallel, 
    yielding d<sub>v</sub>-dimensional output values. These are concatenated and once again 
    projected, resulting in the final values, as depicted in Figure 2.</p>
    
    <p>Multi-head attention allows the model to jointly attend to information from different 
    representation subspaces at different positions. With a single attention head, averaging 
    inhibits this.</p>
    
    <div class="equation">
        MultiHead(Q, K, V) = Concat(head<sub>1</sub>, ..., head<sub>h</sub>)W<sup>O</sup>
    </div>
    
    <p>where head<sub>i</sub> = Attention(QW<sub>i</sub><sup>Q</sup>, KW<sub>i</sub><sup>K</sup>, 
    VW<sub>i</sub><sup>V</sup>)</p>
    
    <h2>3.3 Position-wise Feed-Forward Networks</h2>
    
    <p>In addition to attention sub-layers, each of the layers in our encoder and decoder 
    contains a fully connected feed-forward network, which is applied to each position 
    separately and identically. This consists of two linear transformations with a ReLU 
    activation in between.</p>
    
    <div class="equation">
        FFN(x) = max(0, xW<sub>1</sub> + b<sub>1</sub>)W<sub>2</sub> + b<sub>2</sub>
    </div>
    
    <h2>3.4 Embeddings and Softmax</h2>
    
    <p>Similarly to other sequence transduction models, we use learned embeddings to convert 
    the input tokens and output tokens to vectors of dimension d<sub>model</sub>. We also 
    use the usual learned linear transformation and softmax function to convert the decoder 
    output to predicted next-token probabilities. In our model, we share the same weight 
    matrix between the two embedding layers and the pre-softmax linear transformation. In 
    the embedding layers, we multiply those weights by √d<sub>model</sub>.</p>
    
    <h2>3.5 Positional Encoding</h2>
    
    <p>Since our model contains no recurrence and no convolution, in order for the model 
    to make use of the order of the sequence, we must inject some information about the 
    relative or absolute position of the tokens in the sequence. To this end, we add 
    "positional encodings" to the input embeddings at the bottoms of the encoder and decoder 
    stacks. The positional encodings have the same dimension d<sub>model</sub> as the 
    embeddings, so that the two can be summed. There are many choices of positional 
    encodings, learned and fixed.</p>
    
    <p>In this work, we use sine and cosine functions of different frequencies:</p>
    
    <div class="equation">
        PE<sub>(pos,2i)</sub> = sin(pos / 10000<sup>2i/d<sub>model</sub></sup>)
    </div>
    
    <div class="equation">
        PE<sub>(pos,2i+1)</sub> = cos(pos / 10000<sup>2i/d<sub>model</sub></sup>)
    </div>
    
    <p>where pos is the position and i is the dimension. That is, each dimension of the 
    positional encoding corresponds to a sinusoid. The wavelengths form a geometric 
    progression from 2π to 10000 · 2π. We chose this function because we hypothesized it 
    would allow the model to easily learn to attend by relative positions, since for any 
    fixed offset k, PE<sub>pos+k</sub> can be represented as a linear function of 
    PE<sub>pos</sub>.</p>
    
    <h1>Why Self-Attention</h1>
    
    <p>In this section we compare various aspects of self-attention layers to the recurrent 
    and convolutional layers commonly used for mapping one variable-length sequence of 
    symbol representations (x<sub>1</sub>, ..., x<sub>n</sub>) to another sequence of equal 
    length (z<sub>1</sub>, ..., z<sub>n</sub>), with x<sub>i</sub>, z<sub>i</sub> ∈ R<sup>d</sup>, 
    such as a hidden layer in a typical sequence transduction encoder or decoder. Motivating 
    our use of self-attention we consider three desiderata.</p>
    
    <p>One is the total computational complexity per layer. Another is the amount of 
    computation that can be parallelized, as measured by the minimum number of sequential 
    operations required. The third is the path length between long-range dependencies in 
    the network. Learning long-range dependencies is a key challenge in many sequence 
    transduction tasks. One key factor affecting the ability to learn such dependencies 
    is the length of the paths forward and backward signals have to traverse in the network. 
    The shorter these paths between any combination of positions in the input and output 
    sequences, the easier it is to learn long-range dependencies.</p>
    
    <h1>Training</h1>
    
    <h2>5.1 Training Data and Batching</h2>
    
    <p>We trained on the standard WMT 2014 English-German dataset consisting of about 4.5 
    million sentence pairs. Sentences were encoded using byte-pair encoding, which has a 
    shared source-target vocabulary of about 37000 tokens. For English-French, we used the 
    significantly larger WMT 2014 English-French dataset consisting of 36M sentences and 
    split tokens into a 32000 word-piece vocabulary.</p>
    
    <h2>5.2 Hardware and Schedule</h2>
    
    <p>We trained our models on one machine with 8 NVIDIA P100 GPUs. For our base models 
    using the hyperparameters described throughout the paper, each training step took about 
    0.4 seconds. We trained the base models for a total of 100,000 steps or 12 hours. For 
    our big models, step time was 1.0 seconds. The big models were trained for 300,000 steps 
    (3.5 days).</p>
    
    <h2>5.3 Optimizer</h2>
    
    <p>We used the Adam optimizer with β<sub>1</sub> = 0.9, β<sub>2</sub> = 0.98 and 
    ε = 10<sup>-9</sup>. We varied the learning rate over the course of training, 
    increasing it linearly for the first warmup_steps training steps, and decreasing it 
    thereafter proportionally to the inverse square root of the step number. We set 
    warmup_steps = 4000.</p>
    
    <h2>5.4 Regularization</h2>
    
    <p>We employ three types of regularization during training:</p>
    
    <p><strong>Residual Dropout</strong> We apply dropout to the output of each sub-layer, 
    before it is added to the sub-layer input and normalized. In addition, we apply dropout 
    to the sums of the embeddings and the positional encodings in both the encoder and 
    decoder stacks. For the base model, we use a rate of P<sub>drop</sub> = 0.1.</p>
    
    <p><strong>Label Smoothing</strong> During training, we employed label smoothing of 
    value ε<sub>ls</sub> = 0.1. This hurts perplexity, as the model learns to be more 
    uncertain, but improves accuracy and BLEU score.</p>
    
    <h1>Results</h1>
    
    <h2>6.1 Machine Translation</h2>
    
    <p>On the WMT 2014 English-to-German translation task, the big transformer model 
    (Transformer (big) in Table 2) outperforms the best previously reported models 
    (including ensembles) by more than 2.0 BLEU, establishing a new state-of-the-art 
    BLEU score of 28.4. The configuration of this model is listed in the bottom line 
    of Table 3. Training took 3.5 days on 8 P100 GPUs, even though our model has 
    significantly more parameters, training cost is a small fraction of the 
    convolutional sequence to sequence models from the literature.</p>
    
    <p>On the WMT 2014 English-to-French translation task, our big model achieves a 
    BLEU score of 41.8, outperforming all of the previously published single models, 
    at less than 1/4 the training cost of the previous state-of-the-art model. The 
    Transformer (big) model trained for English-to-French used dropout rate 
    P<sub>drop</sub> = 0.1, instead of 0.3.</p>
    
    <h2>6.2 Model Variations</h2>
    
    <p>To evaluate the importance of different components of the Transformer, we varied 
    our base model in different ways, measuring the performance change on English-to-German 
    translation development set, newstest2013. In Table 3 (row A) we change the number 
    of attention heads and the attention key and value dimensions, keeping the amount of 
    computation constant. While single-head attention is 0.9 BLEU worse than the best 
    setting, quality also drops off with too many heads.</p>
    
    <h1>Conclusion</h1>
    
    <p>In this work, we presented the Transformer, the first sequence transduction model 
    based entirely on attention, replacing the recurrent layers most commonly used in 
    encoder-decoder architectures with multi-headed self-attention.</p>
    
    <p>For translation tasks, the Transformer can be trained significantly faster than 
    architectures based on recurrent or convolutional layers. On both WMT 2014 
    English-to-German and WMT 2014 English-to-French translation tasks, we achieve a 
    new state of the art. In the former task our best model outperforms even all 
    previously reported ensembles.</p>
    
    <p>We are excited about the future of attention-based models and plan to apply them 
    to other tasks. We plan to extend the Transformer to problems involving input and 
    output modalities other than text and to investigate local, restricted attention 
    mechanisms to efficiently handle large inputs and outputs such as images, audio and 
    video. Making generation less sequential is another research goals of ours.</p>
    """

    references = [
        "[1] Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio. Neural machine translation by jointly learning to align and translate. CoRR, abs/1409.0473, 2014.",
        "[2] Denny Britz, Anna Goldie, Minh-Thang Luong, and Quoc Le. Massive exploration of neural machine translation architectures. CoRR, abs/1703.03906, 2017.",
        "[3] Junyoung Chung, Caglar Gulcehre, KyungHyun Cho, and Yoshua Bengio. Empirical evaluation of gated recurrent neural networks on sequence modeling. CoRR, abs/1412.3555, 2014.",
        "[4] Kyunghyun Cho, Bart van Merrienboer, Caglar Gulcehre, Fethi Bougares, Holger Schwenk, and Yoshua Bengio. Learning phrase representations using RNN encoder-decoder for statistical machine translation. CoRR, abs/1406.1078, 2014.",
        "[5] Francois Chollet. Xception: Deep learning with depthwise separable convolutions. CoRR, abs/1610.02357, 2016.",
        "[6] Mostafa Dehghani, Stephan Gouws, Oriol Vinyals, Jakob Uszkoreit, and Łukasz Kaiser. Universal transformers. CoRR, abs/1807.03819, 2018.",
        "[7] Chris Dyer, Victor Chahuneau, and Noah A. Smith. A simple, fast, and effective reparameterization of IBM model 2. In Proceedings of NAACL, 2013.",
        "[8] Jonas Gehring, Michael Auli, David Grangier, Denis Yarats, and Yann N. Dauphin. Convolutional sequence to sequence learning. CoRR, abs/1705.03122, 2017.",
        "[9] Alex Graves. Generating sequences with recurrent neural networks. CoRR, abs/1308.0850, 2013.",
        "[10] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. CoRR, abs/1512.03385, 2015.",
        "[11] Sepp Hochreiter and Jürgen Schmidhuber. Long short-term memory. Neural Computation, 9(8):1735–1780, 1997.",
        "[12] Rafal Jozefowicz, Oriol Vinyals, Mike Schuster, Noam Shazeer, and Yonghui Wu. Exploring the limits of language modeling. CoRR, abs/1602.02410, 2016.",
        "[13] Łukasz Kaiser and Samy Bengio. Can active memory replace attention? In Advances in Neural Information Processing Systems, 2016.",
        "[14] Nal Kalchbrenner, Lasse Espeholt, Karen Simonyan, Aaron van den Oord, Alex Graves, and Koray Kavukcuoglu. Neural machine translation in linear time. CoRR, abs/1610.10099, 2016.",
        "[15] Nal Kalchbrenner and Phil Blunsom. Recurrent continuous translation models. In Proceedings of EMNLP, 2013.",
        "[16] Yoon Kim, Carl Denton, Luong Hoang, and Alexander M. Rush. Structured attention networks. CoRR, abs/1702.00887, 2017.",
        "[17] Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization. CoRR, abs/1412.6980, 2014.",
        "[18] Oleksii Kuchaiev and Boris Ginsburg. Factorization tricks for LSTM networks. CoRR, abs/1703.10722, 2017.",
        "[19] Zhouhan Lin, Minwei Feng, Cicero Nogueira dos Santos, Mo Yu, Bing Xiang, Bowen Zhou, and Yoshua Bengio. A structured self-attentive sentence embedding. CoRR, abs/1703.03130, 2017.",
        "[20] Thang Luong, Hieu Pham, and Christopher D. Manning. Effective approaches to attention-based neural machine translation. CoRR, abs/1508.04025, 2015.",
        "[21] Mitchell P. Marcus, Mary Ann Marcinkiewicz, and Beatrice Santorini. Building a large annotated corpus of English: The Penn Treebank. Computational Linguistics, 19(2):313–330, 1993.",
        "[22] David McClosky, Eugene Charniak, and Mark Johnson. Effective self-training for parsing. In Proceedings of NAACL, 2006.",
        "[23] Ankur Parikh, Oscar Täckström, Dipanjan Das, and Jakob Uszkoreit. A decomposable attention model for natural language inference. CoRR, abs/1606.01933, 2016.",
        "[24] Romain Paulus, Caiming Xiong, and Richard Socher. A deep reinforced model for abstractive summarization. CoRR, abs/1705.04304, 2017.",
        "[25] Ofir Press and Lior Wolf. Using the output embedding to improve language models. CoRR, abs/1608.05859, 2016.",
        "[26] Rico Sennrich, Barry Haddow, and Alexandra Birch. Neural machine translation of rare words with subword units. CoRR, abs/1508.07909, 2015.",
        "[27] Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton, and Jeff Dean. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. CoRR, abs/1701.06538, 2017.",
        "[28] Ilya Sutskever, Oriol Vinyals, and Quoc V. Le. Sequence to sequence learning with neural networks. In Advances in Neural Information Processing Systems, 2014.",
        "[29] Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jonathon Shlens, and Zbigniew Wojna. Rethinking the inception architecture for computer vision. CoRR, abs/1512.00567, 2015.",
        "[30] Christian Szegedy, Sergey Ioffe, Vincent Vanhoucke, and Alexander A. Alemi. Inception-v4, inception-resnet and the impact of residual connections on learning. CoRR, abs/1602.07261, 2016.",
        "[31] Zhaopeng Tu, Yang Liu, Lifeng Shang, Xiaohua Liu, and Hang Li. Neural machine translation with reconstruction. CoRR, abs/1611.01874, 2016.",
        "[32] Ashish Vaswani, Yinggong Zhao, Victoria Fossum, and David Chiang. Decoding with large-scale neural language models improves translation. In Proceedings of EMNLP, 2013.",
        "[33] Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc V. Le, Mohammad Norouzi, Wolfgang Macherey, Maxim Krikun, Yuan Cao, Qin Gao, Klaus Macherey, et al. Google's neural machine translation system: Bridging the gap between human and machine translation. CoRR, abs/1609.08144, 2016.",
        "[34] Jie Zhou, Ying Cao, Xuguang Wang, Peng Li, and Wei Xu. Deep recurrent models with fast-forward connections for neural machine translation. CoRR, abs/1606.04199, 2016.",
        "[35] Barret Zoph and Kevin Knight. Multi-source neural translation. CoRR, abs/1601.00710, 2016.",
    ]

    # Generate the paper
    output_path = Path("attention_is_all_you_need_recreated.pdf")

    print("📄 Generating 'Attention Is All You Need' paper...")
    print(f"   Title: {title}")
    print(f"   Authors: {len(authors)} authors")
    print(f"   Output: {output_path}")

    generate_academic_paper(
        title=title,
        content=content,
        output_path=output_path,
        abstract=abstract.strip(),
        authors=authors,
        affiliations=affiliations,
        conference="NIPS",
        year="2017",
        references=references,
    )

    print("\n✅ Paper generated successfully!")
    print(f"   📄 {output_path.absolute()}")

    return output_path


if __name__ == "__main__":
    main()

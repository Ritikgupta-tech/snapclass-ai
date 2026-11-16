# SNAPCLASS AI — Official Technical References, Literature Citations & Glossary

**Course:** B.Tech Computer Science & Engineering  
**Project:** SNAPCLASS AI  
**Document Purpose:** Academic Bibliography, Technical Documentation Links, and Glossary of Engineering Terminology.  

---

## 1. Academic Research Literature (IEEE Reference Style)

1. **F. Schroff, D. Kalenichenko, and J. Philbin**, "FaceNet: A unified embedding for face recognition and clustering," in *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, Boston, MA, USA, 2015, pp. 815–823.  
   *Significance to Project:* Establishes the mathematical foundation for mapping facial images directly to compact 128-dimensional Euclidean spaces where squared $L_2$ distances directly correspond to facial similarity.
2. **D. E. King**, "Dlib-ml: A Machine Learning Toolkit," *Journal of Machine Learning Research (JMLR)*, vol. 10, pp. 1755–1758, 2009.  
   *Significance to Project:* Primary algorithmic library utilized in `src/pipelines/face_pipeline.py` for HOG frontal face detection, 68-point facial landmark shape prediction, and ResNet metric inference.
3. **D. E. King**, "Max-margin object detection," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2015, pp. 1921–1929.  
   *Significance to Project:* Details the optimization framework behind dlib's robust face localization under varying lighting and pose conditions.
4. **L. Wan, Q. Wang, A. Papir, and I. L. Moreno**, "Generalized End-to-End Loss for Speaker Verification," in *IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, Calgary, AB, Canada, 2018, pp. 4879–4883.  
   *Significance to Project:* Core theoretical architecture implemented by Resemblyzer, providing the 3-layer LSTM Voice Encoder that maps speech waveforms into 256-dimensional speaker embeddings.
5. **N. Dalal and B. Triggs**, "Histograms of oriented gradients for human detection," in *IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR)*, San Diego, CA, USA, 2005, vol. 1, pp. 886–893.  
   *Significance to Project:* Algorithmic basis of the initial facial detection step in classroom crowd photography.
6. **B. McFee, C. Raffel, D. Liang, D. P. Ellis, M. McVicar, E. Battenberg, and O. Nieto**, "librosa: Audio and Music Signal Analysis in Python," in *Proceedings of the 14th Python in Science Conference*, 2015, pp. 18–25.  
   *Significance to Project:* Audio signal processing library utilized for 16,000 Hz resampling, non-silent frame splitting, and Voice Activity Detection in `src/pipelines/voice_pipeline.py`.
7. **P. Provos and D. Mazières**, "A Future-Adaptable Password Scheme," in *USENIX Annual Technical Conference, FREENIX Track*, Monterey, CA, USA, 1999, pp. 81–92.  
   *Significance to Project:* Establishes the bcrypt adaptive salted key derivation function utilized in `src/database/db.py` for teacher credential security.

---

## 2. Official Technology Documentation & Repositories

| Software / Tool | Governing Entity / Author | Official Documentation / Repository URL |
| :--- | :--- | :--- |
| **Python Language** | Python Software Foundation | [https://docs.python.org/3.12/](https://docs.python.org/3.12/) |
| **Streamlit Framework** | Snowflake Inc. | [https://docs.streamlit.io/](https://docs.streamlit.io/) |
| **Supabase Platform** | Supabase Inc. | [https://supabase.com/docs](https://supabase.com/docs) |
| **PostgreSQL Database** | PostgreSQL Global Development Group | [https://www.postgresql.org/docs/15/](https://www.postgresql.org/docs/15/) |
| **dlib C++ Toolkit** | Davis E. King | [http://dlib.net/](http://dlib.net/) |
| **face_recognition** | Adam Geitgey | [https://github.com/ageitgey/face_recognition](https://github.com/ageitgey/face_recognition) |
| **Resemblyzer** | Corentin Jemine | [https://github.com/resemble-ai/Resemblyzer](https://github.com/resemble-ai/Resemblyzer) |
| **PyTorch (torch)** | Linux Foundation / PyTorch Team | [https://pytorch.org/docs/stable/](https://pytorch.org/docs/stable/) |
| **librosa** | Brian McFee et al. | [https://librosa.org/doc/latest/](https://librosa.org/doc/latest/) |
| **scikit-learn** | scikit-learn developers | [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/) |
| **bcrypt** | Python Cryptographic Authority (PyCA) | [https://github.com/pyca/bcrypt/](https://github.com/pyca/bcrypt/) |
| **Segno QR Generator** | Lars Bilke | [https://segno.readthedocs.io/](https://segno.readthedocs.io/) |
| **Pillow (PIL Fork)** | Jeffrey A. Clark (Alex Clark) et al. | [https://pillow.readthedocs.io/](https://pillow.readthedocs.io/) |
| **Pytest** | Holger Krekel et al. | [https://docs.pytest.org/](https://docs.pytest.org/) |
| **Docker Platform** | Docker Inc. | [https://docs.docker.com/](https://docs.docker.com/) |

---

## 3. Glossary of Academic & Technical Terminology

- **Affine Transformation**: A geometric transformation that preserves collinearity and ratios of distances, utilized during facial alignment to standardize pupil and nose positioning regardless of tilt.
- **Bcrypt**: An adaptive password hashing function based on the Blowfish symmetric cipher, incorporating an explicit work factor (iteration count) and per-user cryptographic salting to prevent rainbow table attacks.
- **Biometric Embedding**: A low-dimensional continuous vector representation generated by a deep neural network, positioned on a unit hypersphere such that semantic biometric similarity is directly measured by distance or angle.
- **Cosine Similarity**: A metric measuring the cosine of the angle between two multi-dimensional vectors in an inner product space, invariant to vector magnitude: $\cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\|_2 \|\mathbf{B}\|_2}$.
- **dlib 68-Point Landmark Model**: An ensemble of randomized regression trees that predicts the $(x, y)$ coordinates of 68 physiological facial landmarks (eyebrows, eyes, nose bridge, jawline, and lips).
- **Euclidean Distance ($L_2$ Norm)**: The straight-line distance between two points in Euclidean space: $\|\mathbf{x} - \mathbf{y}\|_2 = \sqrt{\sum (x_i - y_i)^2}$.
- **Histogram of Oriented Gradients (HOG)**: A computer vision feature descriptor that counts occurrences of edge gradient orientations in localized portions of an image, widely utilized for object and face localization.
- **Idempotency**: An API and architectural property where performing an operation multiple times produces the identical side-effect as performing it once, preventing duplicate record creation upon multiple client clicks.
- **Long Short-Term Memory (LSTM)**: A specialized recurrent neural network (RNN) architecture incorporating input, forget, and output gates, capable of capturing long-range acoustic temporal dependencies in spoken speech waveforms.
- **PostgREST**: A standalone web server that automatically translates a PostgreSQL database schema into a secure, RESTful API over HTTPS.
- **Rate Limiting**: A cybersecurity throttling mechanism that restricts the frequency of client requests (e.g., maximum 5 login attempts per 300 seconds) to mitigate brute-force and dictionary attacks.
- **ResNet (Residual Neural Network)**: A deep convolutional network architecture featuring skip (identity) connections, mitigating the vanishing gradient problem and enabling training of deep metric feature extractors.
- **Row Level Security (RLS)**: A PostgreSQL security mechanism that filters database rows returned by queries based on the identity and privileges of the authenticated requesting user.
- **Surrogate Key**: An artificially generated unique identifier (e.g., an auto-incrementing `BIGINT` or `UUID`) assigned to a database record, independent of business meaning.
- **Voice Activity Detection (VAD)**: An audio analysis technique that identifies the presence or absence of human speech in an acoustic stream, filtering out background silence and noise.

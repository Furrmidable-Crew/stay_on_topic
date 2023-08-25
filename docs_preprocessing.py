from langchain.text_splitter import RecursiveCharacterTextSplitter

from cat.mad_hatter.decorators import hook


@hook
def rabbithole_splits_text(text, chunk_size, chunk_overlap, cat):
    # text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\\n\\n", "\n\n", ".\\n", ".\n", "\\n", "\n", " ", ""],
    )

    # split text
    docs = text_splitter.split_documents(text)

    # remove short texts (page numbers, isolated words, etc.)
    docs = list(filter(lambda d: len(d.page_content) > 10, docs))

    # remove text made of only numbers
    idx = [i for i, d in enumerate(docs) if d.page_content.replace(" ", "").replace("\n", "").isnumeric()]
    docs = [docs[i] for i in range(len(docs)) if i not in idx]

    return docs

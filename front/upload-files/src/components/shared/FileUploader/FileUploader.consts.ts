export const UPLOAD_FILES_ENDPOINT = `${process.env.REACT_APP_API_ENDPOINT}/${process.env.REACT_APP_ENV}/files`;
export const LOCALE_SINGLE_WORDS = { strings: { done: "Quitar" } };
export const COMPRESSOR_LOCALE_SINGLE_WORDS = {
  strings: {
    compressingImages: "Comprimiendo imagen...",
    compressedX: "Ahorro de %{size} al comprimir imagen",
  },
};
export const EXCEEDS_SIZE_MESSAGE = "La imagen excede el tamaño de 100mb";
export const MAX_FILE_SIZE = 100000000;
export const MAX_FILE_MULTIPART_SIZE = 100 * 2 ** 20;
export const QUALITY = 0.1;
export const FILES_TYPES = [".csv"];

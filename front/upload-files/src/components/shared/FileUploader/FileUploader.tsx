import AwsS3 from "@uppy/aws-s3";
import Compressor from "@uppy/compressor";
import Uppy from "@uppy/core";
import Spanish from "@uppy/locales/lib/es_MX";
import { Dashboard } from "@uppy/react";
import { useState } from "react";
import { FileUploaderProps } from "./FileUploader.types";

import "@uppy/core/dist/style.min.css";
import "@uppy/dashboard/dist/style.min.css";
import "@uppy/status-bar/dist/style.min.css";
import {
  COMPRESSOR_LOCALE_SINGLE_WORDS,
  EXCEEDS_SIZE_MESSAGE,
  FILES_TYPES,
  LOCALE_SINGLE_WORDS,
  MAX_FILE_MULTIPART_SIZE,
  MAX_FILE_SIZE,
  QUALITY,
  UPLOAD_FILES_ENDPOINT,
} from "./FileUploader.consts";

Spanish.strings.exceedsSize = EXCEEDS_SIZE_MESSAGE;

const FileUploader = (props: FileUploaderProps) => {
  const { width, height, maxNumberOfFiles, filename } = props;

  const [uppy] = useState(() =>
    new Uppy({
      debug: process.env.REACT_APP_ENV !== "prod",
      locale: Spanish,
      autoProceed: true,
      restrictions: {
        maxNumberOfFiles: maxNumberOfFiles,
        maxFileSize: MAX_FILE_SIZE,
        allowedFileTypes: FILES_TYPES,
      },
      onBeforeFileAdded: (currentFile) => {
        const name = `${filename}.${currentFile.extension}`;
        const modifiedFile = {
          ...currentFile,
          meta: {
            ...currentFile.meta,
            name,
          },
          name,
        };
        return modifiedFile;
      },
    })
      .use(AwsS3, {
        shouldUseMultipart: (file) => file.size > MAX_FILE_MULTIPART_SIZE,
        companionUrl: UPLOAD_FILES_ENDPOINT,
      })
      .use(Compressor, {
        locale: COMPRESSOR_LOCALE_SINGLE_WORDS,
        quality: QUALITY,
      })
  );

  return (
    <Dashboard
      uppy={uppy}
      width={width}
      height={height}
      locale={LOCALE_SINGLE_WORDS}
    />
  );
};

export default FileUploader;

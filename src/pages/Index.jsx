import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const Index = () => {
  const [url, setUrl] = useState("");
  const [downloadLink, setDownloadLink] = useState("");

  const generateDownloadLink = () => {
    // Assuming the download link is the same as the input URL for now
    setDownloadLink(url);
  };

  return (
    <div className="h-screen w-screen flex items-center justify-center">
      <div className="p-4 max-w-md w-full">
        <h1 className="text-3xl text-center mb-4">Download Link Generator</h1>
        <div className="mb-4">
          <Input
            type="text"
            placeholder="Enter URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full"
          />
        </div>
        <div className="text-center">
          <Button onClick={generateDownloadLink}>Generate Download Link</Button>
        </div>
        {downloadLink && (
          <div className="mt-4 text-center">
            <a href={downloadLink} className="text-blue-500" target="_blank" rel="noopener noreferrer">
              {downloadLink}
            </a>
          </div>
        )}
      </div>
    </div>
  );
};

export default Index;
type FileUploadProps = {
    onFileSelect: (file: File | null) => void;
};

export default function FileUpload({ onFileSelect }: FileUploadProps) {
    return (
        <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Upload File</label>
            <input
                type="file"
                accept=".pdf,.docx"
                onChange={(e) => onFileSelect(e.target.files?.[0] || null)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400"
            />
        </div>
    );
}
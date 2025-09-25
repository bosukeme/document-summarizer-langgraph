type FormatSelectProps = {
    value: string;
    onChange: (value: string) => void;
};

export default function FormatSelect({ value, onChange }: FormatSelectProps) {
    return (
        <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Summary Style</label>
            <select
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-400"
            >
                <option value="narrative">Narrative</option>
                <option value="bullets">Bullets</option>
            </select>
        </div>
    );
}

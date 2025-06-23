
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

interface CodeInputProps {
  onSubmit: (code: string) => void;
  isProcessing: boolean;
}

const CodeInput: React.FC<CodeInputProps> = ({ onSubmit, isProcessing }) => {
  const [code, setCode] = useState('');

  const handleSubmit = () => {
    if (code.trim()) {
      onSubmit(code);
    }
  };

  return (
    <div className="bg-amber-950/80 border border-amber-700/50 rounded-lg p-3 shadow-xl backdrop-blur-xs">
      <h2 className="text-sm font-semibold text-amber-100 mb-2">Submit Your Code</h2>
      <Textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Enter your code here for review by the AI courtroom..."
        className="min-h-[60px] font-mono text-xs bg-amber-950/60 border-amber-700/40 text-amber-100 placeholder:text-amber-400 focus:border-amber-500"
        disabled={isProcessing}
      />
      <div className="flex justify-end mt-2">
        <Button 
          onClick={handleSubmit}
          disabled={!code.trim() || isProcessing}
          className="bg-amber-700 hover:bg-amber-600 text-amber-100 border border-amber-600"
        >
          {isProcessing ? 'Processing...' : 'Submit to Courtroom'}
        </Button>
      </div>
    </div>
  );
};

export default CodeInput;

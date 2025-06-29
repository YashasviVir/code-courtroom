import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import Index from "@/pages/Index";

function App() {
  return (
    <>
      <TooltipProvider>
        <Toaster />
        <Index />
      </TooltipProvider>
    </>
  );
}

export default App;

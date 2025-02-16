import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

interface ToolsModalProps {
  open: boolean
  onClose: () => void
}

export function ToolsModal({ open, onClose }: ToolsModalProps) {
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="bg-[#fcfbef]/90">
        <DialogHeader>
          <DialogTitle>Tools</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="flex justify-between items-center">
              <span>Name of Tool</span>
              <Button variant="secondary" size="sm">
                Reload
              </Button>
            </div>
          ))}
        </div>
      </DialogContent>
    </Dialog>
  )
}


import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

interface APICredentialsModalProps {
  open: boolean
  onClose: () => void
}

export function APICredentialsModal({ open, onClose }: APICredentialsModalProps) {
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="bg-[#f1c0e8]/90">
        <DialogHeader>
          <DialogTitle>API Credentials</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <p>Why does Chronological need access</p>
          <Button className="w-full" variant="secondary">
            Go To: <a href="#">Settings</a> {/*Replaced <Name> with a functional <a> tag*/}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}


export interface Question {
    id: number
    text: string
}

export interface Answer {
    id: number
    text: string
    question_id: number
}
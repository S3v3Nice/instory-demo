export interface User {
    id: bigint
    username: string
    email: string
    date_verified_email: string | null
    avatar: string | null
    first_name: string | null
    last_name: string | null
    date_joined: string
    posts_count?: number
    followers_count?: number
    following_count?: number
}

export interface Follower {
    follower: User
    date_created: string
}

export interface Following {
    following: User
    date_created: string
}

export interface Post {
    id: bigint
    user: User
    image: string
    description: string | null
    date_created: string
    is_liked: boolean
    likes_count: number
    comments_count: number
}
